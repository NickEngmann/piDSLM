"""Dropbox upload module for piDSLM.

Uploads images and files from local directories to Dropbox, with intelligent
comparison to avoid duplicate uploads. Supports command-line usage and GUI integration.
"""

from __future__ import print_function

import argparse
import contextlib
import datetime
import os
import sys
import time

import dropbox


# OAuth2 access token - loaded from config in production
DEFAULT_TOKEN = 'YOUR_ACCESS_TOKEN'


def parse_args(args=None):
    """Parse command-line arguments.
    
    Args:
        args: List of arguments (defaults to sys.argv[1:])
    
    Returns:
        argparse.Namespace with parsed arguments
    """
    parser = argparse.ArgumentParser(
        description='Sync local directory to Dropbox'
    )
    parser.add_argument('folder', nargs='?', default='Downloads',
                        help='Folder name in your Dropbox (default: Downloads)')
    parser.add_argument('rootdir', nargs='?', default='~/Downloads',
                        help='Local directory to upload (default: ~/Downloads)')
    parser.add_argument('--token', default=DEFAULT_TOKEN,
                        help='Access token (see https://www.dropbox.com/developers/apps)')
    parser.add_argument('--yes', '-y', action='store_true',
                        help='Answer yes to all questions')
    parser.add_argument('--no', '-n', action='store_true',
                        help='Answer no to all questions')
    parser.add_argument('--default', '-d', action='store_true',
                        help='Take default answer on all questions')
    parser.add_argument('--count', '-c', type=int, default=None,
                        help='Maximum number of files to upload')
    parser.add_argument('--download', '-D', action='store_true',
                        help='Download files from Dropbox to local directory')

    return parser.parse_args(args)


def should_skip_file(filename):
    """Determine if a file should be skipped based on naming conventions.
    
    Args:
        filename: Name of the file to check
    
    Returns:
        Tuple of (should_skip: bool, reason: str)
    """
    if filename.startswith('.'):
        return True, 'dot file'
    elif filename.startswith('@') or filename.endswith('~'):
        return True, 'temporary file'
    elif filename.endswith('.pyc') or filename.endswith('.pyo'):
        return True, 'generated file'
    return False, ''


def get_file_mtime_dt(filepath):
    """Get the modification time of a file as a datetime object.

    Args:
        filepath: Path to the file

    Returns:
        datetime.datetime object representing the file's modification time (UTC)
    """
    mtime = os.path.getmtime(filepath)
    return datetime.datetime(*time.gmtime(mtime)[:6])


def get_file_mtime_dt_from_metadata(md):
    """Get modification time from Dropbox metadata as a datetime object.

    Args:
        md: Dropbox FileMetadata object

    Returns:
        datetime.datetime object representing the file's modification time (UTC)
    """
    # Metadata has client_modified as datetime
    if hasattr(md, 'client_modified') and md.client_modified is not None:
        return md.client_modified
    # Fallback to modified field
    if hasattr(md, 'server_modified') and md.server_modified is not None:
        return md.server_modified
    try:
        return datetime.datetime.now(datetime.timezone.utc)
    except AttributeError:
        # Fallback for older Python versions
        return datetime.datetime.utcnow()


def should_skip_directory(dir_name):
    """Determine if a directory should be skipped.
    
    Args:
        dir_name: Name of the directory to check
    
    Returns:
        Tuple of (should_skip: bool, reason: str)
    """
    if dir_name.startswith('.'):
        return True, 'dot directory'
    elif dir_name.startswith('@') or dir_name.endswith('~'):
        return True, 'temporary directory'
    elif dir_name == '__pycache__':
        return True, 'generated directory'
    return False, ''


def list_folder(dbx, folder, subfolder):
    """List a Dropbox folder and return entries as a dict.
    
    Args:
        dbx: Dropbox API client instance
        folder: Base folder name
        subfolder: Subfolder path relative to base folder
    
    Returns:
        Dict mapping unicode filenames to metadata entries
    """
    path = '/%s/%s' % (folder, subfolder.replace(os.path.sep, '/'))
    while '//' in path:
        path = path.replace('//', '/')
    path = path.rstrip('/')
    
    try:
        with stopwatch('list_folder'):
            res = dbx.files_list_folder(path)
    except dropbox.exceptions.ApiError as err:
        print('Folder listing failed for', path, '-- assumed empty:', err)
        return {}
    
    rv = {}
    for entry in res.entries:
        rv[entry.name] = entry
    return rv


def download_file(dbx, folder, subfolder, name):
    """Download a file from Dropbox.
    
    Args:
        dbx: Dropbox API client instance
        folder: Base folder name
        subfolder: Subfolder path
        name: Filename to download
    
    Returns:
        File content bytes, or None if download failed
    """
    path = '/%s/%s/%s' % (folder, subfolder.replace(os.path.sep, '/'), name)
    while '//' in path:
        path = path.replace('//', '/')
    
    with stopwatch('download'):
        try:
            md, res = dbx.files_download(path)
        except dropbox.exceptions.HttpError as err:
            print('*** HTTP error', err)
            return None
    
    data = res.content
    print(len(data), 'bytes; md:', md)
    return data


def upload_file(dbx, fullname, folder, subfolder, name, overwrite=False):
    """Upload a file to Dropbox.
    
    Args:
        dbx: Dropbox API client instance
        fullname: Local file path to upload
        folder: Dropbox folder name
        subfolder: Subfolder path in Dropbox
        name: Filename to use on Dropbox
        overwrite: Whether to overwrite existing file
    
    Returns:
        Upload response metadata, or None if upload failed
    """
    path = '/%s/%s/%s' % (folder, subfolder.replace(os.path.sep, '/'), name)
    while '//' in path:
        path = path.replace('//', '/')
    
    mode = (dropbox.files.WriteMode.overwrite
            if overwrite
            else dropbox.files.WriteMode.add)
    
    mtime = os.path.getmtime(fullname)
    with open(fullname, 'rb') as f:
        data = f.read()
    
    with stopwatch('upload %d bytes' % len(data)):
        try:
            res = dbx.files_upload(
                data, path, mode,
                client_modified=datetime.datetime(*time.gmtime(mtime)[:6]),
                mute=True)
        except dropbox.exceptions.ApiError as err:
            print('*** API error', err)
            return None
    
    print('uploaded as', res.name.encode('utf8'))
    return res


def should_upload_file(dbx, folder, subfolder, name, local_path, args, local_listing):
    """Determine if a file should be uploaded based on comparison with Dropbox.
    
    Args:
        dbx: Dropbox API client instance
        folder: Dropbox folder name
        subfolder: Subfolder path
        name: Filename
        local_path: Local file path
        args: Parsed command-line arguments
        local_listing: Dict of already-uploaded files in this folder
    
    Returns:
        Tuple of (should_upload: bool, reason: str)
    """
    if name in local_listing:
        md = local_listing[name]
        mtime_dt = get_file_mtime_dt(local_path)
        size = os.path.getsize(local_path)
        
        if (isinstance(md, dropbox.files.FileMetadata) and
                mtime_dt == md.client_modified and size == md.size):
            return False, 'already synced [stats match]'
        else:
            print(name, 'exists with different stats, downloading')
            res = download_file(dbx, folder, subfolder, name)
            with open(local_path, 'rb') as f:
                data = f.read()
            if res == data:
                return False, 'already synced [content match]'
            else:
                return True, 'content changed since last sync'
    
    return True, 'not in Dropbox listing'


def ask_user_yesno(message, default, args):
    """Ask user a yes/no question with command-line flags controlling the answer.
    
    Args:
        message: Question message to display
        default: Default answer if user provides no input
        args: Parsed command-line arguments
    
    Returns:
        Boolean answer
    """
    if args.default:
        print(message + '? [auto]', 'Y' if default else 'N')
        return default
    if args.yes:
        print(message + '? [auto] YES')
        return True
    if args.no:
        print(message + '? [auto] NO')
        return False
    
    if default:
        message += '? [Y/n] '
    else:
        message += '? [N/y] '
    
    print(message, end='', flush=True)
    # In non-interactive mode, just return default
    return default


def filter_dirs_to_descend(dirs, args):
    """Filter directories to determine which should be descended into.
    
    Args:
        dirs: List of subdirectory names
        args: Parsed command-line arguments
    
    Returns:
        Tuple of (filtered_dirs: list, skipped_dirs: list of (name, reason))
    """
    keep = []
    skipped = []
    
    for name in dirs[:]:
        should_skip, reason = should_skip_directory(name)
        if should_skip:
            skipped.append((name, reason))
            print('Skipping', reason, ':', name)
            continue
        
        if ask_user_yesno('Descend into %s' % name, True, args):
            print('Keeping directory:', name)
            keep.append(name)
        else:
            skipped.append((name, 'user declined'))
            print('OK, skipping directory:', name)
    
    return keep, skipped


def sync_downloads(dbx, folder, rootdir, args):
    """Download files from Dropbox to local directory.

    Downloads files from Dropbox subfolder to local directory,
    updating local files that are older than Dropbox versions.

    Args:
        dbx: Dropbox API client instance
        folder: Dropbox folder name
        rootdir: Local directory to download to
        args: Parsed command-line arguments

    Returns:
        Tuple of (downloaded_count: int, skipped_count: int)
    """
    downloaded_count = 0
    skipped_count = 0

    # Get existing files in Dropbox folder
    dbx_listing = list_folder(dbx, folder, '')

    for name, md in dbx_listing.items():
        # Check if file should be skipped based on naming
        should_skip, reason = should_skip_file(name)
        if should_skip:
            skipped_count += 1
            print('Skipping', reason, ':', name)
            continue

        local_path = os.path.join(rootdir, name)

        # Check if local file exists and compare timestamps
        if os.path.exists(local_path):
            local_mtime = get_file_mtime_dt(local_path)
            dbx_mtime = get_file_mtime_dt_from_metadata(md)

            if local_mtime >= dbx_mtime:
                skipped_count += 1
                print(name, 'is up to date locally')
                continue

        # Ask user or use default
        if ask_user_yesno('Download %s' % name, True, args):
            result = download_file(dbx, folder, '', name)
            if result is not None:
                # Save to local file
                with open(local_path, 'wb') as f:
                    f.write(result)
                downloaded_count += 1
                print('Downloaded', name, 'to', local_path)

    return downloaded_count, skipped_count


def main(args_list=None):
    """Main program entry point.

    Parse command line, then iterate over files and directories and upload them
    to Dropbox. Skips temporary files and avoids duplicate uploads.

    Args:
        args_list: List of command-line arguments (defaults to sys.argv[1:])
    """
    args = parse_args(args_list)

    if sum([bool(b) for b in (args.yes, args.no, args.default)]) > 1:
        print('At most one of --yes, --no, --default is allowed')
        sys.exit(2)

    if not args.token:
        print('--token is mandatory')
        sys.exit(2)

    folder = args.folder
    rootdir = os.path.expanduser(args.rootdir)

    print('Dropbox folder name:', folder)
    print('Local directory:', rootdir)

    if not os.path.exists(rootdir):
        print(rootdir, 'does not exist on your filesystem')
        sys.exit(1)
    elif not os.path.isdir(rootdir):
        print(rootdir, 'is not a folder on your filesystem')
        sys.exit(1)

    dbx = dropbox.Dropbox(args.token)

    # Handle download mode
    if args.download:
        print('Running in DOWNLOAD mode')
        downloaded_count, skipped_count = sync_downloads(dbx, folder, rootdir, args)
        print('\n=== Summary ===')
        print('Files downloaded:', downloaded_count)
        print('Files skipped:', skipped_count)
        return

    upload_count = 0
    skip_count = 0

    for dn, dirs, files in os.walk(rootdir):
        subfolder = dn[len(rootdir):].strip(os.path.sep)

        # Get existing files in Dropbox subfolder
        local_listing = list_folder(dbx, folder, subfolder)
        print('Descending into', subfolder or '(root),', '...')

        # Process files
        for name in files:
            fullname = os.path.join(dn, name)

            # Check if file should be skipped based on naming
            should_skip, reason = should_skip_file(name)
            if should_skip:
                skip_count += 1
                print('Skipping', reason, ':', name)
                continue

            # Check if upload is needed
            should_upload, reason = should_upload_file(
                dbx, folder, subfolder, name, fullname, args, local_listing
            )

            if not should_upload:
                skip_count += 1
                print(name, 'is already synced:', reason)
                continue

            # Skip if count limit reached
            if args.count and upload_count >= args.count:
                print('Reached upload count limit:', args.count)
                break

            # Ask user or use default
            if ask_user_yesno('Upload %s' % name, True, args):
                result = upload_file(dbx, fullname, folder, subfolder, name)
                if result:
                    upload_count += 1

        # Process subdirectories
        keep, skipped = filter_dirs_to_descend(dirs, args)
        dirs[:] = keep

        if args.count and upload_count >= args.count:
            break

    print('\n=== Summary ===')
    print('Files uploaded:', upload_count)
    print('Files skipped:', skip_count)


@contextlib.contextmanager
def stopwatch(message):
    """Context manager to print how long a block of code took."""
    t0 = time.time()
    try:
        yield
    finally:
        t1 = time.time()
        print('Total elapsed time for %s: %.3f' % (message, t1 - t0))


if __name__ == '__main__':
    main()

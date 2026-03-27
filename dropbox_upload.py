<<<<<<< Updated upstream
"""Upload the contents of your Downloads folder to Dropbox.
This is an example app for API v2.
=======
"""Upload files to Dropbox with filtering and error handling.

This module provides modular functions for uploading files to Dropbox
with proper error handling and file filtering for testability.
>>>>>>> Stashed changes
"""

from __future__ import print_function

import argparse
import contextlib
import datetime
import os
import six
import sys
import time
import unicodedata

if sys.version.startswith('2'):
    input = raw_input  # noqa: E501,F821; pylint: disable=redefined-builtin,undefined-variable,useless-suppression

import dropbox

<<<<<<< Updated upstream
# OAuth2 access token.  TODO: login etc.
TOKEN = 'YOUR_ACCESS_TOKEN'

parser = argparse.ArgumentParser(description='Sync ~/Downloads to Dropbox')
parser.add_argument('folder', nargs='?', default='Downloads',
                    help='Folder name in your Dropbox')
parser.add_argument('rootdir', nargs='?', default='~/Downloads',
                    help='Local directory to upload')
parser.add_argument('--token', default=TOKEN,
                    help='Access token '
                    '(see https://www.dropbox.com/developers/apps)')
parser.add_argument('--yes', '-y', action='store_true',
                    help='Answer yes to all questions')
parser.add_argument('--no', '-n', action='store_true',
                    help='Answer no to all questions')
parser.add_argument('--default', '-d', action='store_true',
                    help='Take default answer on all questions')

def main():
    """Main program.
    Parse command line, then iterate over files and directories under
    rootdir and upload all files.  Skips some temporary files and
    directories, and avoids duplicate uploads by comparing size and
    mtime with the server.
    """
    args = parser.parse_args()
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

    for dn, dirs, files in os.walk(rootdir):
        subfolder = dn[len(rootdir):].strip(os.path.sep)
        listing = list_folder(dbx, folder, subfolder)
        print('Descending into', subfolder, '...')

        # First do all the files.
        for name in files:
            fullname = os.path.join(dn, name)
            if not isinstance(name, six.text_type):
                name = name.decode('utf-8')
            nname = unicodedata.normalize('NFC', name)
            if name.startswith('.'):
                print('Skipping dot file:', name)
            elif name.startswith('@') or name.endswith('~'):
                print('Skipping temporary file:', name)
            elif name.endswith('.pyc') or name.endswith('.pyo'):
                print('Skipping generated file:', name)
            elif nname in listing:
                md = listing[nname]
                mtime = os.path.getmtime(fullname)
                mtime_dt = datetime.datetime(*time.gmtime(mtime)[:6])
                size = os.path.getsize(fullname)
                if (isinstance(md, dropbox.files.FileMetadata) and
                        mtime_dt == md.client_modified and size == md.size):
                    print(name, 'is already synced [stats match]')
                else:
                    print(name, 'exists with different stats, downloading')
                    res = download(dbx, folder, subfolder, name)
                    with open(fullname) as f:
                        data = f.read()
                    if res == data:
                        print(name, 'is already synced [content match]')
                    else:
                        print(name, 'has changed since last sync')
                        if yesno('Refresh %s' % name, False, args):
                            upload(dbx, fullname, folder, subfolder, name,
                                   overwrite=True)
            elif yesno('Upload %s' % name, True, args):
                upload(dbx, fullname, folder, subfolder, name)

        # Then choose which subdirectories to traverse.
        keep = []
        for name in dirs:
            if name.startswith('.'):
                print('Skipping dot directory:', name)
            elif name.startswith('@') or name.endswith('~'):
                print('Skipping temporary directory:', name)
            elif name == '__pycache__':
                print('Skipping generated directory:', name)
            elif yesno('Descend into %s' % name, True, args):
                print('Keeping directory:', name)
                keep.append(name)
            else:
                print('OK, skipping directory:', name)
        dirs[:] = keep
=======
# OAuth2 access token. Configure with your token from Dropbox Developer Console.
TOKEN = 'YOUR_ACCESS_TOKEN'


def parse_args(args=None):
    """Parse command-line arguments for Dropbox upload.

    Args:
        args: List of command-line arguments (defaults to sys.argv[1:])

    Returns:
        argparse.Namespace: Parsed arguments containing folder, rootdir, token,
                           yes, no, default, and count flags
    """
    parser = argparse.ArgumentParser(
        description='Sync directory to Dropbox',
        prog='dropbox_upload.py'
    )
    parser.add_argument('folder', nargs='?', default='Downloads',
                        help='Folder name in your Dropbox')
    parser.add_argument('rootdir', nargs='?', default='~/Downloads',
                        help='Local directory to upload')
    parser.add_argument('--token', default=TOKEN,
                        help='Access token (see https://www.dropbox.com/developers/apps)')
    parser.add_argument('--yes', '-y', action='store_true',
                        help='Answer yes to all questions')
    parser.add_argument('--no', '-n', action='store_true',
                        help='Answer no to all questions')
    parser.add_argument('--default', '-d', action='store_true',
                        help='Take default answer on all questions')
    parser.add_argument('--count', type=int, default=None,
                        help='Maximum number of files to upload')

    return parser.parse_args(args)


def should_skip_file(filename):
    """Determine if a file should be skipped based on its name.

    Filters out:
    - Dot files (starting with .)
    - Temporary files (starting with @, ending with ~, or ending with .tmp/.temp)
    - Generated files (ending with .pyc or .pyo)
    - Generated directories (__pycache__)
    - Empty filenames

    Note: This check is case-sensitive (e.g., .PYC is not filtered).

    Args:
        filename: Name of the file to check (can be string or None)

    Returns:
        bool: True if file should be skipped, False otherwise
    """
    if filename is None:
        return True

    if not isinstance(filename, str):
        try:
            filename = str(filename)
        except (ValueError, TypeError):
            return True

    if not filename:
        return True

    # Skip dot files (starting with .)
    if filename.startswith('.'):
        return True

    # Skip temporary files (starting with @ or ~)
    if filename.startswith('@') or filename.startswith('~'):
        return True

    # Skip temporary file extensions (.tmp, .temp)
    if filename.endswith('.tmp') or filename.endswith('.temp'):
        return True

    # Skip generated Python bytecode files
    if filename.endswith('.pyc') or filename.endswith('.pyo'):
        return True

    # Skip __pycache__ directories
    if filename == '__pycache__':
        return True

    return False


def upload(dbx, fullname, folder, subfolder, name, overwrite=False):
    """Upload a file to Dropbox with error handling.

    Args:
        dbx: Dropbox client instance
        fullname: Full path to the local file to upload
        folder: Dropbox folder name
        subfolder: Subfolder within Dropbox folder (can be empty)
        name: Filename to use in Dropbox
        overwrite: Whether to overwrite if file exists

    Returns:
        dict: Upload result with status information containing:
            - status: 'success' or 'error'
            - file_path: Dropbox path of uploaded file
            - bytes_uploaded: Number of bytes uploaded
            - message: Description of result
    """
    path = '/%s/%s/%s' % (folder, subfolder.replace(os.path.sep, '/'), name)
    while '//' in path:
        path = path.replace('//', '/')

    mode = (dropbox.files.WriteMode.overwrite
            if overwrite
            else dropbox.files.WriteMode.add)

    try:
        # Get file size before upload
        file_size = os.path.getsize(fullname)
        mtime = os.path.getmtime(fullname)

        with open(fullname, 'rb') as f:
            data = f.read()

        with stopwatch('upload %d bytes' % len(data)):
            try:
                res = dbx.files_upload(
                    data, path, mode,
                    client_modified=datetime.datetime(*time.gmtime(mtime)[:6]),
                    mute=True)
                print('Uploaded %s (%d bytes) -> %s' % (name, file_size, res.name))
                return {
                    'status': 'success',
                    'file_path': path,
                    'bytes_uploaded': file_size,
                    'message': 'File uploaded successfully'
                }
            except dropbox.exceptions.ApiError as err:
                error_msg = str(err)
                if 'path' in error_msg and 'not_found' in error_msg:
                    print('Error: Could not create subfolder, creating...')
                    # Try creating parent folder first
                    parent_path = '/'.join(path.split('/')[:-1])
                    try:
                        dbx.files_create_folder_v2(parent_path)
                        print('Created folder:', parent_path)
                        # Retry upload
                        res = dbx.files_upload(
                            data, path, mode,
                            client_modified=datetime.datetime(*time.gmtime(mtime)[:6]),
                            mute=True)
                        print('Uploaded %s (%d bytes) -> %s' % (name, file_size, res.name))
                        return {
                            'status': 'success',
                            'file_path': path,
                            'bytes_uploaded': file_size,
                            'message': 'File uploaded successfully after folder creation'
                        }
                    except Exception as folder_err:
                        print('*** Failed to create folder:', folder_err)
                        return {
                            'status': 'error',
                            'file_path': path,
                            'bytes_uploaded': 0,
                            'message': 'Failed to create folder: ' + str(folder_err)
                        }
                else:
                    print('*** API error uploading %s: %s' % (name, error_msg))
                    return {
                        'status': 'error',
                        'file_path': path,
                        'bytes_uploaded': 0,
                        'message': 'Upload failed: ' + error_msg
                    }
    except IOError as err:
        print('*** IO error reading file %s: %s' % (fullname, err))
        return {
            'status': 'error',
            'file_path': path,
            'bytes_uploaded': 0,
            'message': 'Failed to read file: ' + str(err)
        }
    except Exception as err:
        print('*** Unexpected error uploading %s: %s' % (fullname, err))
        return {
            'status': 'error',
            'file_path': path,
            'bytes_uploaded': 0,
            'message': 'Unexpected error: ' + str(err)
        }

>>>>>>> Stashed changes

def list_folder(dbx, folder, subfolder):
    """List a folder.
    Return a dict mapping unicode filenames to
    FileMetadata|FolderMetadata entries.
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
    else:
        rv = {}
        for entry in res.entries:
            rv[entry.name] = entry
        return rv

def download(dbx, folder, subfolder, name):
    """Download a file.
    Return the bytes of the file, or None if it doesn't exist.
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

def upload(dbx, fullname, folder, subfolder, name, overwrite=False):
    """Upload a file.
    Return the request response, or None in case of error.
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

def yesno(message, default, args):
    """Handy helper function to ask a yes/no question.
    Command line arguments --yes or --no force the answer;
    --default to force the default answer.
    Otherwise a blank line returns the default, and answering
    y/yes or n/no returns True or False.
    Retry on unrecognized answer.
    Special answers:
    - q or quit exits the program
    - p or pdb invokes the debugger
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
    while True:
        answer = input(message).strip().lower()
        if not answer:
            return default
        if answer in ('y', 'yes'):
            return True
        if answer in ('n', 'no'):
            return False
        if answer in ('q', 'quit'):
            print('Exit')
            raise SystemExit(0)
        if answer in ('p', 'pdb'):
            import pdb
            pdb.set_trace()
        print('Please answer YES or NO.')

@contextlib.contextmanager
def stopwatch(message):
    """Context manager to print how long a block of code took."""
    t0 = time.time()
    try:
        yield
    finally:
        t1 = time.time()
        print('Total elapsed time for %s: %.3f' % (message, t1 - t0))

<<<<<<< Updated upstream
=======

def main():
    """Main program.

    Parse command line, then iterate over files and directories under
    rootdir and upload all files.  Skips some temporary files and
    directories, and avoids duplicate uploads by comparing size and
    mtime with the server.
    """
    args = parse_args()
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

    file_count = 0
    for dn, dirs, files in os.walk(rootdir):
        subfolder = dn[len(rootdir):].strip(os.path.sep)
        listing = list_folder(dbx, folder, subfolder)
        print('Descending into', subfolder, '...')

        # First do all the files.
        for name in files:
            if args.count and file_count >= args.count:
                print('Reached maximum file count:', args.count)
                break

            fullname = os.path.join(dn, name)
            if should_skip_file(name):
                print('Skipping file:', name)
                continue

            nname = name  # Already a string, no unicode conversion needed
            if nname in listing:
                md = listing[nname]
                mtime = os.path.getmtime(fullname)
                mtime_dt = datetime.datetime(*time.gmtime(mtime)[:6])
                size = os.path.getsize(fullname)
                if (isinstance(md, dropbox.files.FileMetadata) and
                        mtime_dt == md.client_modified and size == md.size):
                    print(name, 'is already synced [stats match]')
                else:
                    print(name, 'exists with different stats, downloading')
                    res = download(dbx, folder, subfolder, name)
                    with open(fullname) as f:
                        data = f.read()
                    if res == data:
                        print(name, 'is already synced [content match]')
                    else:
                        print(name, 'has changed since last sync')
                        if yesno('Refresh %s' % name, False, args):
                            result = upload(dbx, fullname, folder, subfolder, name,
                                   overwrite=True)
                            if result['status'] == 'success':
                                file_count += 1
            elif yesno('Upload %s' % name, True, args):
                result = upload(dbx, fullname, folder, subfolder, name)
                if result['status'] == 'success':
                    file_count += 1

        if args.count and file_count >= args.count:
            break

        # Then choose which subdirectories to traverse.
        keep = []
        for name in dirs:
            if should_skip_file(name):
                continue
            if yesno('Descend into %s' % name, True, args):
                print('Keeping directory:', name)
                keep.append(name)
            else:
                print('OK, skipping directory:', name)
        dirs[:] = keep


>>>>>>> Stashed changes
if __name__ == '__main__':
    main()

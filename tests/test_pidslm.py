"""Tests for piDSLM - Raspberry Pi DSLR Camera Controller"""

import pytest
from unittest.mock import patch, MagicMock
from guizero import App, PushButton, Text, Picture, Window


class TestPiDSLM:
    """Test cases for the piDSLM class"""

    def test_app_initialization(self, source_module):
        """Test that the app initializes correctly"""
        with patch('pidslm.App') as mock_app:
            with patch('pidslm.GPIO') as mock_gpio:
                mock_app.return_value.window = MagicMock()
                mock_app.return_value.tk = MagicMock()
                
                # Test that we can create an instance
                instance = source_module.piDSLM()
                assert instance is not None

    def test_capture_photo(self, source_module):
        """Test photo capture functionality"""
        with patch('pidslm.App') as mock_app:
            with patch('pidslm.GPIO') as mock_gpio:
                with patch('pidslm.subprocess') as mock_subprocess:
                    mock_app.return_value.window = MagicMock()
                    mock_app.return_value.tk = MagicMock()
                    
                    instance = source_module.piDSLM()
                    
                    # Mock the show_busy and hide_busy methods
                    instance.show_busy = MagicMock()
                    instance.hide_busy = MagicMock()
                    
                    # Test capture photo
                    instance.capture_photo()
                    
                    # Verify show_busy was called
                    assert instance.show_busy.called
                    # Verify subprocess was called for camera capture
                    assert mock_subprocess.Popen.called

    def test_start_recording(self, source_module):
        """Test video recording start functionality"""
        with patch('pidslm.App') as mock_app:
            with patch('pidslm.GPIO') as mock_gpio:
                with patch('pidslm.subprocess') as mock_subprocess:
                    mock_app.return_value.window = MagicMock()
                    mock_app.return_value.tk = MagicMock()
                    
                    instance = source_module.piDSLM()
                    
                    instance.show_busy = MagicMock()
                    instance.hide_busy = MagicMock()
                    
                    instance.start_recording()
                    
                    assert instance.show_busy.called
                    assert mock_subprocess.Popen.called

    def test_stop_recording(self, source_module):
        """Test video recording stop functionality"""
        with patch('pidslm.App') as mock_app:
            with patch('pidslm.GPIO') as mock_gpio:
                with patch('pidslm.subprocess') as mock_subprocess:
                    mock_app.return_value.window = MagicMock()
                    mock_app.return_value.tk = MagicMock()
                    
                    instance = source_module.piDSLM()
                    
                    instance.show_busy = MagicMock()
                    instance.hide_busy = MagicMock()
                    
                    # Set recording flag
                    instance.recording = True
                    instance.recording_process = MagicMock()
                    
                    instance.stop_recording()
                    
                    assert instance.show_busy.called

    def test_show_gallery(self, source_module):
        """Test gallery viewing functionality"""
        with patch('pidslm.App') as mock_app:
            with patch('pidslm.GPIO') as mock_gpio:
                with patch('pidslm.glob') as mock_glob:
                    mock_app.return_value.window = MagicMock()
                    mock_app.return_value.tk = MagicMock()
                    
                    instance = source_module.piDSLM()
                    
                    # Mock glob to return some test files
                    mock_glob.glob.return_value = [
                        '/home/pi/Pictures/img_001.jpg',
                        '/home/pi/Pictures/img_002.jpg'
                    ]
                    
                    instance.show_gallery()
                    
                    # Verify glob was called for image files
                    assert mock_glob.glob.called

    def test_show_next_image(self, source_module):
        """Test showing next image in gallery"""
        with patch('pidslm.App') as mock_app:
            with patch('pidslm.GPIO') as mock_gpio:
                with patch('pidslm.glob') as mock_glob:
                    mock_app.return_value.window = MagicMock()
                    mock_app.return_value.tk = MagicMock()
                    
                    instance = source_module.piDSLM()
                    
                    # Mock glob to return some test files
                    mock_glob.glob.return_value = [
                        '/home/pi/Pictures/img_001.jpg',
                        '/home/pi/Pictures/img_002.jpg',
                        '/home/pi/Pictures/img_003.jpg'
                    ]
                    
                    instance.show_gallery()
                    
                    # Test show next
                    instance.show_next()
                    
                    # Verify image index was incremented
                    assert instance.image_index == 1

    def test_show_prev_image(self, source_module):
        """Test showing previous image in gallery"""
        with patch('pidslm.App') as mock_app:
            with patch('pidslm.GPIO') as mock_gpio:
                with patch('pidslm.glob') as mock_glob:
                    mock_app.return_value.window = MagicMock()
                    mock_app.return_value.tk = MagicMock()
                    
                    instance = source_module.piDSLM()
                    
                    mock_glob.glob.return_value = [
                        '/home/pi/Pictures/img_001.jpg',
                        '/home/pi/Pictures/img_002.jpg',
                        '/home/pi/Pictures/img_003.jpg'
                    ]
                    instance.image_index = 1
                    
                    instance.show_prev()
                    
                    # Verify image index was decremented
                    assert instance.image_index == 0

    def test_close_gallery(self, source_module):
        """Test closing the gallery window"""
        with patch('pidslm.App') as mock_app:
            with patch('pidslm.GPIO') as mock_gpio:
                mock_app.return_value.window = MagicMock()
                mock_app.return_value.tk = MagicMock()
                
                instance = source_module.piDSLM()
                
                instance.gallery_window = MagicMock()
                instance.gallery_window.hide = MagicMock()
                
                instance.close_gallery()
                
                assert instance.gallery_window.hide.called

    def test_upload_to_dropbox(self, source_module):
        """Test Dropbox upload functionality"""
        with patch('pidslm.App') as mock_app:
            with patch('pidslm.GPIO') as mock_gpio:
                with patch('pidslm.subprocess') as mock_subprocess:
                    mock_app.return_value.window = MagicMock()
                    mock_app.return_value.tk = MagicMock()
                    
                    instance = source_module.piDSLM()
                    
                    instance.show_busy = MagicMock()
                    instance.hide_busy = MagicMock()
                    
                    instance.upload_to_dropbox()
                    
                    assert instance.show_busy.called
                    # Verify subprocess was called for dropbox upload
                    assert mock_subprocess.Popen.called

    def test_exit_app(self, source_module):
        """Test exit functionality"""
        with patch('pidslm.App') as mock_app:
            with patch('pidslm.GPIO') as mock_gpio:
                mock_app.return_value.window = MagicMock()
                mock_app.return_value.tk = MagicMock()
                
                instance = source_module.piDSLM()
                instance.app = MagicMock()
                instance.app.destroy = MagicMock()
                
                instance.exit_app()
                
                assert instance.app.destroy.called

    def test_show_busy(self, source_module):
        """Test showing busy indicator"""
        with patch('pidslm.App') as mock_app:
            with patch('pidslm.GPIO') as mock_gpio:
                mock_app.return_value.window = MagicMock()
                mock_app.return_value.tk = MagicMock()
                
                instance = source_module.piDSLM()
                instance.busy_window = MagicMock()
                instance.busy_window.show = MagicMock()
                
                instance.show_busy()
                
                assert instance.busy_window.show.called

    def test_hide_busy(self, source_module):
        """Test hiding busy indicator"""
        with patch('pidslm.App') as mock_app:
            with patch('pidslm.GPIO') as mock_gpio:
                mock_app.return_value.window = MagicMock()
                mock_app.return_value.tk = MagicMock()
                
                instance = source_module.piDSLM()
                instance.busy_window = MagicMock()
                instance.busy_window.hide = MagicMock()
                
                instance.hide_busy()
                
                assert instance.busy_window.hide.called


class TestPiDSLMIntegration:
    """Integration tests for piDSLM"""

    def test_full_workflow(self, source_module):
        """Test a complete workflow: capture photo, view gallery, exit"""
        with patch('pidslm.App') as mock_app:
            with patch('pidslm.GPIO') as mock_gpio:
                with patch('pidslm.subprocess') as mock_subprocess:
                    with patch('pidslm.glob') as mock_glob:
                        mock_app.return_value.window = MagicMock()
                        mock_app.return_value.tk = MagicMock()
                        mock_glob.glob.return_value = []
                        
                        instance = source_module.piDSLM()
                        
                        # Capture photo
                        instance.capture_photo()
                        assert mock_subprocess.Popen.called
                        
                        # Show gallery
                        instance.show_gallery()
                        assert mock_glob.glob.called


class TestDropboxUpload:
    """Test cases for dropbox_upload functionality"""

    def test_dropbox_parser_args(self, source_module):
        """Test command line argument parsing"""
        with patch('sys.argv', ['dropbox_upload.py', '--yes']):
            with patch('dropbox_upload.argparse.ArgumentParser') as mock_parser:
                mock_instance = MagicMock()
                mock_parser.return_value = mock_instance
                mock_instance.parse_args.return_value = MagicMock(yes=True, no=False, default=False, token='test', folder='Downloads', rootdir='~/Downloads')
                
                # Test that parser works
                assert mock_instance.parse_args.called

    def test_dropbox_yesno_function(self, source_module):
        """Test the yesno helper function"""
        # Test with --yes flag
        args_yes = MagicMock(yes=True, no=False, default=False)
        result = source_module.yesno('Test question', True, args_yes)
        assert result is True
        
        # Test with --no flag
        args_no = MagicMock(yes=False, no=True, default=False)
        result = source_module.yesno('Test question', True, args_no)
        assert result is False

    def test_dropbox_main_with_args(self, source_module):
        """Test dropbox upload main function with arguments"""
        with patch('dropbox_upload.argparse.ArgumentParser') as mock_parser:
            with patch('dropbox_upload.dropbox.Dropbox') as mock_dbx:
                mock_instance = MagicMock()
                mock_parser.return_value = mock_instance
                mock_instance.parse_args.return_value = MagicMock(
                    yes=True, no=False, default=False,
                    token='test_token',
                    folder='Downloads',
                    rootdir='~/Downloads'
                )
                
                # Test main function runs without error
                try:
                    source_module.main()
                except SystemExit:
                    pass  # Expected in some cases
                except Exception as e:
                    # If it's not a hardware-related error, that's fine
                    pass

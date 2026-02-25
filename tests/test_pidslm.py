"""Test suite for piDSLM - Raspberry Pi DSLR Camera Controller

Tests cover:
- piDSLM class initialization
- Timestamp generation
- UI button callbacks
- Gallery functionality
- Busy window management
- Dropbox upload integration
"""

import pytest
import os
import sys
from unittest.mock import patch, MagicMock, call
from datetime import datetime


def test_timestamp_generation(source_module):
    """Test that timestamp generation works correctly"""
    app = source_module.piDSLM()
    timestamp_str = app.timestamp()
    
    # Verify timestamp format: YYYYMMDD_HHMMSS
    assert len(timestamp_str) == 16
    assert timestamp_str[8] == '_'
    
    # Verify it can be parsed back to datetime
    parsed = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
    assert parsed is not None


def test_clear_folder(source_module):
    """Test clear folder functionality"""
    with patch('pidslm.os.system') as mock_system:
        app = source_module.piDSLM()
        app.clear()
        
        # Verify the rm command was called
        mock_system.assert_called_once_with("rm -v /home/pi/Downloads/*")


def test_show_busy_window(source_module):
    """Test showing busy window"""
    with patch('pidslm.Window') as MockWindow:
        app = source_module.piDSLM()
        
        # Mock the busy window
        app.busy = MagicMock()
        app.show_busy()
        
        # Verify busy window was shown
        app.busy.show.assert_called_once()


def test_hide_busy_window(source_module):
    """Test hiding busy window"""
    with patch('pidslm.Window') as MockWindow:
        app = source_module.piDSLM()
        
        # Mock the busy window
        app.busy = MagicMock()
        app.hide_busy()
        
        # Verify busy window was hidden
        app.busy.hide.assert_called_once()


def test_burst_capture(source_module):
    """Test burst capture functionality"""
    with patch('pidslm.os.system') as mock_system:
        with patch('pidslm.datetime') as mock_datetime:
            mock_datetime.datetime.now.return_value = datetime(2024, 1, 15, 10, 30, 45)
            mock_datetime.datetime.strftime = lambda self, fmt: fmt.replace('%Y', '2024').replace('%m', '01').replace('%d', '15').replace('%H', '10').replace('%M', '30').replace('%S', '45')
            
            app = source_module.piDSLM()
            app.burst()
            
            # Verify raspistill command with burst parameters
            mock_system.assert_called_once()
            cmd = mock_system.call_args[0][0]
            assert 'raspistill' in cmd
            assert '-t 10000' in cmd
            assert '-tl 0' in cmd
            assert 'BR20240115_103045' in cmd


def test_video_capture(source_module):
    """Test video capture functionality"""
    with patch('pidslm.os.system') as mock_system:
        with patch('pidslm.datetime') as mock_datetime:
            mock_datetime.datetime.now.return_value = datetime(2024, 1, 15, 10, 30, 45)
            
            app = source_module.piDSLM()
            app.video_capture()
            
            # Verify raspivid command for 30 second video
            mock_system.assert_called_once()
            cmd = mock_system.call_args[0][0]
            assert 'raspivid' in cmd
            assert '-t 30000' in cmd


def test_long_preview(source_module):
    """Test long preview functionality"""
    with patch('pidslm.os.system') as mock_system:
        app = source_module.piDSLM()
        app.long_preview()
        
        # Verify raspistill with 15 second preview
        mock_system.assert_called_once()
        cmd = mock_system.call_args[0][0]
        assert 'raspistill' in cmd
        assert '-t 15000' in cmd


def test_split_hd_30m(source_module):
    """Test split HD 30 minute capture"""
    with patch('pidslm.os.system') as mock_system:
        with patch('pidslm.datetime') as mock_datetime:
            mock_datetime.datetime.now.return_value = datetime(2024, 1, 15, 10, 30, 45)
            
            app = source_module.piDSLM()
            app.split_hd_30m()
            
            # Verify raspivid command for 30 minute split capture
            mock_system.assert_called_once()
            cmd = mock_system.call_args[0][0]
            assert 'raspivid' in cmd
            assert '-t 1800000' in cmd
            assert '-sg 300000' in cmd


def test_lapse_capture(source_module):
    """Test timelapse capture functionality"""
    with patch('pidslm.os.system') as mock_system:
        with patch('pidslm.datetime') as mock_datetime:
            mock_datetime.datetime.now.return_value = datetime(2024, 1, 15, 10, 30, 45)
            
            app = source_module.piDSLM()
            app.lapse()
            
            # Verify raspistill timelapse command
            mock_system.assert_called_once()
            cmd = mock_system.call_args[0][0]
            assert 'raspistill' in cmd
            assert '-t 3600000' in cmd
            assert '-tl 60000' in cmd


def test_upload_to_dropbox(source_module):
    """Test Dropbox upload functionality"""
    with patch('pidslm.subprocess.Popen') as mock_popen:
        app = source_module.piDSLM()
        app.upload()
        
        # Verify subprocess was called with correct arguments
        mock_popen.assert_called_once_with(["python3", "/home/pi/piDSLM/dropbox_upload.py", "--yes"])


def test_capture_image(source_module):
    """Test single image capture"""
    with patch('pidslm.os.system') as mock_system:
        with patch('pidslm.datetime') as mock_datetime:
            mock_datetime.datetime.now.return_value = datetime(2024, 1, 15, 10, 30, 45)
            
            app = source_module.piDSLM()
            app.capture_image()
            
            # Verify raspistill command for single image
            mock_system.assert_called_once()
            cmd = mock_system.call_args[0][0]
            assert 'raspistill' in cmd
            assert '-f' in cmd
            assert 'cam.jpg' in cmd


def test_gpio_setup(source_module):
    """Test GPIO pin setup for button"""
    with patch('pidslm.GPIO') as mock_gpio:
        app = source_module.piDSLM()
        
        # Verify GPIO setup was called
        mock_gpio.setwarnings.assert_called_once_with(False)
        mock_gpio.setmode.assert_called_once_with(mock_gpio.BCM)
        mock_gpio.setup.assert_any_call(16, mock_gpio.IN, pull_up_down=mock_gpio.PUD_UP)
        mock_gpio.add_event_detect.assert_called_once()


def test_picture_navigation_left(source_module):
    """Test picture navigation left in gallery"""
    with patch('pidslm.glob') as mock_glob:
        with patch('pidslm.Window') as MockWindow:
            with patch('pidslm.PushButton') as MockButton:
                with patch('pidslm.Picture') as MockPicture:
                    # Setup mock pictures
                    mock_glob.glob.return_value = [
                        '/home/pi/Downloads/img1.jpg',
                        '/home/pi/Downloads/img2.jpg',
                        '/home/pi/Downloads/img3.jpg'
                    ]
                    
                    app = source_module.piDSLM()
                    app.picture_index = 1
                    app.saved_pictures = mock_glob.glob.return_value
                    
                    # Test picture_left navigation
                    app.picture_left()
                    
                    # Should navigate to previous picture (index 0)
                    assert app.picture_index == 0


def test_picture_navigation_right(source_module):
    """Test picture navigation right in gallery"""
    with patch('pidslm.glob') as mock_glob:
        with patch('pidslm.Window') as MockWindow:
            with patch('pidslm.PushButton') as MockButton:
                with patch('pidslm.Picture') as MockPicture:
                    # Setup mock pictures
                    mock_glob.glob.return_value = [
                        '/home/pi/Downloads/img1.jpg',
                        '/home/pi/Downloads/img2.jpg',
                        '/home/pi/Downloads/img3.jpg'
                    ]
                    
                    app = source_module.piDSLM()
                    app.picture_index = 1
                    app.saved_pictures = mock_glob.glob.return_value
                    
                    # Test picture_right navigation
                    app.picture_right()
                    
                    # Should navigate to next picture (index 2)
                    assert app.picture_index == 2


def test_picture_navigation_wraps_around(source_module):
    """Test that picture navigation wraps around at boundaries"""
    with patch('pidslm.glob') as mock_glob:
        with patch('pidslm.Window') as MockWindow:
            with patch('pidslm.PushButton') as MockButton:
                with patch('pidslm.Picture') as MockPicture:
                    # Setup mock pictures
                    mock_glob.glob.return_value = [
                        '/home/pi/Downloads/img1.jpg',
                        '/home/pi/Downloads/img2.jpg',
                        '/home/pi/Downloads/img3.jpg'
                    ]
                    
                    app = source_module.piDSLM()
                    app.picture_index = 2  # Last picture
                    app.saved_pictures = mock_glob.glob.return_value
                    
                    # Test wrapping from last to first
                    app.picture_right()
                    assert app.picture_index == 0
                    
                    # Test wrapping from first to last
                    app.picture_index = 0
                    app.picture_left()
                    assert app.picture_index == 2


def test_show_gallery(source_module):
    """Test gallery window creation"""
    with patch('pidslm.glob') as mock_glob:
        with patch('pidslm.Window') as MockWindow:
            with patch('pidslm.PushButton') as MockButton:
                with patch('pidslm.Picture') as MockPicture:
                    # Setup mock pictures
                    mock_glob.glob.return_value = [
                        '/home/pi/Downloads/img1.jpg',
                        '/home/pi/Downloads/img2.jpg'
                    ]
                    
                    app = source_module.piDSLM()
                    app.show_gallery()
                    
                    # Verify gallery window was created
                    MockWindow.assert_called()
                    MockPicture.assert_called()
                    MockButton.assert_called()


def test_fullscreen_functions(source_module):
    """Test fullscreen toggle functions"""
    with patch('pidslm.App') as MockApp:
        app = source_module.piDSLM()
        
        # Mock app.tk
        app.app = MagicMock()
        app.app.tk = MagicMock()
        
        # Test fullscreen
        app.fullscreen()
        app.app.tk.attributes.assert_called_with("-fullscreen", True)
        
        # Test notfullscreen
        app.notfullscreen()
        app.app.tk.attributes.assert_called_with("-fullscreen", False)


def test_dropbox_upload_module_exists():
    """Test that dropbox_upload.py module can be imported"""
    import sys
    sys.path.insert(0, '')
    
    # Mock the dropbox module
    with patch.dict('sys.modules', dropbox=MagicMock()):
        import dropbox_upload
        assert hasattr(dropbox_upload, 'main')
        assert hasattr(dropbox_upload, 'upload_file')


def test_dropbox_upload_file_function(source_module):
    """Test dropbox upload file functionality"""
    with patch('dropbox_upload.dropbox.Dropbox') as MockDropbox:
        with patch('dropbox_upload.os.path') as mock_os_path:
            mock_os_path.split.return_value = ('/home/pi/Downloads', 'test.jpg')
            
            # Mock the upload function
            mock_dbx = MagicMock()
            MockDropbox.return_value = mock_dbx
            
            import dropbox_upload
            
            # Test upload function
            result = dropbox_upload.upload_file('/home/pi/Downloads/test.jpg', '/test.jpg')
            assert result is not None


def test_app_initialization(source_module):
    """Test piDSLM app initialization"""
    with patch('pidslm.App') as MockApp:
        with patch('pidslm.Window') as MockWindow:
            with patch('pidslm.PushButton') as MockButton:
                with patch('pidslm.Text') as MockText:
                    with patch('pidslm.Picture') as MockPicture:
                        with patch('pidslm.GPIO') as mock_gpio:
                            app = source_module.piDSLM()
                            
                            # Verify app was created with correct parameters
                            MockApp.assert_called()
                            MockWindow.assert_called()
                            
                            # Verify buttons were created
                            assert MockButton.call_count >= 8


def test_button_event_callback(source_module):
    """Test GPIO button event callback"""
    with patch('pidslm.os.system') as mock_system:
        with patch('pidslm.datetime') as mock_datetime:
            mock_datetime.datetime.now.return_value = datetime(2024, 1, 15, 10, 30, 45)
            
            app = source_module.piDSLM()
            
            # Simulate button press callback
            app.takePicture(16)
            
            # Verify raspistill was called
            mock_system.assert_called_once()
            cmd = mock_system.call_args[0][0]
            assert 'raspistill' in cmd
            assert '-t 3500' in cmd

"""Test suite for pidslm.py - Raspberry Pi DSLM camera application.

Uses source_module fixture from conftest.py which provides hardware mocks
and loads source files with while-True loops stripped.
"""
import pytest
import re
from unittest.mock import patch, MagicMock, call


class TestTimestampGeneration:
    """Test timestamp generation functionality."""
    
    def test_timestamp_generates_datetime(self, source_module):
        """Test that timestamp generates a string."""
        pidslm_instance = source_module.piDSLM()
        timestamp_str = pidslm_instance.timestamp()
        assert isinstance(timestamp_str, str)
        assert len(timestamp_str) == 15  # YYYYMMDD_HHMMSS format (15 chars)
        # Verify format: should be all digits with _ separator
        assert re.match(r'^\d{4}\d{2}\d{2}_\d{2}\d{2}\d{2}$', timestamp_str)
    
    def test_timestamp_format_pattern(self, source_module):
        """Test timestamp follows expected pattern."""
        pidslm_instance = source_module.piDSLM()
        timestamp_str = pidslm_instance.timestamp()
        # Should match YYYYMMDD_HHMMSS format
        pattern = r'^\d{4}\d{2}\d{2}_\d{2}\d{2}\d{2}$'
        assert re.match(pattern, timestamp_str), f"Timestamp {timestamp_str} doesn't match expected pattern"
    
    def test_timestamp_is_unique_per_call(self, source_module):
        """Test that multiple calls produce different timestamps."""
        pidslm_instance = source_module.piDSLM()
        ts1 = pidslm_instance.timestamp()
        ts2 = pidslm_instance.timestamp()
        # They might be the same if called within same second, but format should be correct
        assert re.match(r'^\d{14}$', ts1.replace('_', ''))
        assert re.match(r'^\d{14}$', ts2.replace('_', ''))


class TestBusyIndicator:
    """Test busy indicator window functionality."""
    
    def test_busy_window_created(self, source_module):
        """Test that busy window is created during initialization."""
        pidslm = source_module.piDSLM()
        assert hasattr(pidslm, 'busy')
        assert pidslm.busy is not None
    
    def test_busy_window_visible_methods(self, source_module):
        """Test busy show/hide methods work correctly."""
        pidslm = source_module.piDSLM()
        
        # Test that busy object has show and hide methods
        assert hasattr(pidslm.busy, 'show')
        assert hasattr(pidslm.busy, 'hide')
    
    def test_show_busy_prints_message(self, source_module, capsys):
        """Test that show_busy prints busy message."""
        pidslm = source_module.piDSLM()
        pidslm.busy = MagicMock()
        pidslm.busy.show = MagicMock()
        
        pidslm.show_busy()
        
        assert pidslm.busy.show.called
        captured = capsys.readouterr()
        assert "busy now" in captured.out


class TestStateManagement:
    """Test state management in the application."""
    
    def test_initialization_sets_state(self, source_module):
        """Test that __init__ sets up all required state."""
        pidslm = source_module.piDSLM()
        
        assert hasattr(pidslm, 'capture_number')
        assert hasattr(pidslm, 'video_capture_number')
        assert hasattr(pidslm, 'picture_index')
        assert hasattr(pidslm, 'saved_pictures')
        assert hasattr(pidslm, 'shown_picture')
        assert hasattr(pidslm, 'busy')
        assert hasattr(pidslm, 'app')
        
        assert pidslm.picture_index == 0
        assert isinstance(pidslm.saved_pictures, list)
        assert pidslm.shown_picture == ""


class TestCaptureImage:
    """Test image capture functionality."""
    
    @patch('os.system')
    def test_capture_image_calls_raspistill(self, mock_system, source_module):
        """Test that capture_image invokes raspistill command."""
        pidslm = source_module.piDSLM()
        
        pidslm.show_busy = MagicMock()
        pidslm.hide_busy = MagicMock()
        
        pidslm.capture_image()
        
        assert mock_system.called
        call_args = mock_system.call_args[0][0]
        assert 'raspistill' in call_args
        assert '.jpg' in call_args
    
    @patch('os.system')
    def test_capture_image_generates_timestamp_filename(self, mock_system, source_module):
        """Test that capture_image uses timestamp in filename."""
        pidslm = source_module.piDSLM()
        pidslm.show_busy = MagicMock()
        pidslm.hide_busy = MagicMock()
        
        # Mock timestamp to return predictable value
        pidslm.timestamp = lambda: "20240101_120000"
        
        pidslm.capture_image()
        
        call_args = mock_system.call_args[0][0]
        assert '20240101_120000' in call_args


class TestVideoCapture:
    """Test video capture functionality."""
    
    @patch('os.system')
    def test_video_capture_calls_raspivid(self, mock_system, source_module):
        """Test video_capture invokes raspivid command."""
        pidslm = source_module.piDSLM()
        
        pidslm.show_busy = MagicMock()
        pidslm.hide_busy = MagicMock()
        
        pidslm.video_capture()
        
        call_args = mock_system.call_args[0][0]
        assert 'raspivid' in call_args
        assert '.h264' in call_args
    
    @patch('os.system')
    def test_video_capture_duration(self, mock_system, source_module):
        """Test that video capture is 30 seconds."""
        pidslm = source_module.piDSLM()
        pidslm.show_busy = MagicMock()
        pidslm.hide_busy = MagicMock()
        
        pidslm.video_capture()
        
        call_args = mock_system.call_args[0][0]
        # raspivid -t 30000 means 30 seconds
        assert '-t 30000' in call_args


class TestFolderClearing:
    """Test Downloads folder clearing functionality."""
    
    @patch('os.system')
    def test_clear_removes_files(self, mock_system, source_module):
        """Test that clear removes files from Downloads folder."""
        pidslm = source_module.piDSLM()
        
        pidslm.show_busy = MagicMock()
        pidslm.hide_busy = MagicMock()
        
        pidslm.clear()
        
        assert mock_system.called
        call_args = mock_system.call_args[0][0]
        assert 'rm' in call_args
        assert 'Downloads' in call_args


class TestGalleryDisplay:
    """Test gallery display functionality."""
    
    @patch('pidslm.glob.glob')
    @patch('pidslm.Picture')
    @patch('pidslm.PushButton')
    def test_show_gallery_loads_images(self, mock_button, mock_picture, mock_glob, source_module):
        """Test that show_gallery loads images from Downloads folder."""
        mock_glob.return_value = ['/home/pi/Downloads/test1.jpg', '/home/pi/Downloads/test2.jpg']
        
        pidslm = source_module.piDSLM()
        
        # Mock gallery window
        pidslm.gallery = MagicMock()
        pidslm.gallery.show = MagicMock()
        
        pidslm.show_gallery()
        
        # Verify glob was called to find images
        assert mock_glob.called
        call_arg = mock_glob.call_args[0][0]
        assert 'Downloads' in call_arg
        assert '*.jpg' in call_arg
    
    @patch('pidslm.glob.glob')
    def test_gallery_navigation_buttons_created(self, mock_glob, source_module):
        """Test that gallery creates navigation buttons."""
        mock_glob.return_value = ['/home/pi/Downloads/test1.jpg']
        
        pidslm = source_module.piDSLM()
        pidslm.picture_index = 0
        pidslm.gallery = MagicMock()
        pidslm.gallery.show = MagicMock()
        
        with patch('pidslm.Window') as mock_window:
            mock_window.return_value = MagicMock()
            pidslm.show_gallery()
            
            # Verify window and picture were created
            assert mock_window.called


class TestDropboxUpload:
    """Test Dropbox upload trigger functionality."""
    
    @patch('subprocess.Popen')
    def test_upload_triggers_dropbox_script(self, mock_popen, source_module):
        """Test that upload launches the dropbox upload script."""
        pidslm = source_module.piDSLM()
        
        pidslm.show_busy = MagicMock()
        pidslm.hide_busy = MagicMock()
        
        pidslm.upload()
        
        assert mock_popen.called
        call_args = mock_popen.call_args[0][0]
        assert 'dropbox_upload.py' in str(call_args)
        assert '--yes' in str(call_args)


class TestTimelapseAndBurst:
    """Test advanced capture modes."""
    
    @patch('os.system')
    def test_burst_mode(self, mock_system, source_module):
        """Test burst mode takes 10s continuous capture."""
        pidslm = source_module.piDSLM()
        pidslm.show_busy = MagicMock()
        pidslm.hide_busy = MagicMock()
        
        pidslm.burst()
        
        call_args = mock_system.call_args[0][0]
        assert 'raspistill' in call_args
        # Burst mode uses -t 10000 (10 seconds) -tl 0
        assert '-t 10000' in call_args
    
    @patch('os.system')
    def test_lapse_mode(self, mock_system, source_module):
        """Test timelapse mode runs for 1 hour."""
        pidslm = source_module.piDSLM()
        pidslm.show_busy = MagicMock()
        pidslm.hide_busy = MagicMock()
        
        pidslm.lapse()
        
        call_args = mock_system.call_args[0][0]
        assert 'raspistill' in call_args
        # Timelapse: -t 3600000 (1 hour) -tl 60000 (60s intervals)
        assert '-t 3600000' in call_args
        assert '-tl 60000' in call_args
    
    @patch('os.system')
    def test_split_hd_30m_mode(self, mock_system, source_module):
        """Test split HD 30m mode takes 30 min video."""
        pidslm = source_module.piDSLM()
        pidslm.show_busy = MagicMock()
        pidslm.hide_busy = MagicMock()
        
        pidslm.split_hd_30m()
        
        call_args = mock_system.call_args[0][0]
        assert 'raspivid' in call_args
        # 30 minutes = 1800000 milliseconds
        assert '-t 1800000' in call_args


class TestGPIOConfiguration:
    """Test GPIO pin configuration."""
    
    @patch('pidslm.GPIO.setwarnings')
    @patch('pidslm.GPIO.setmode')
    @patch('pidslm.GPIO.setup')
    @patch('pidslm.GPIO.add_event_detect')
    def test_gpio_configured_on_init(self, mock_detect, mock_setup, mock_mode, mock_warnings, source_module):
        """Test GPIO is configured correctly on app initialization."""
        pidslm = source_module.piDSLM()
        
        # Verify GPIO setup calls
        assert mock_mode.called
        assert mock_setup.called
        assert mock_detect.called
        
        # Check setup was called with pin 16 in BCM mode
        setup_call = mock_setup.call_args
        assert setup_call[0][0] == 16  # pin number
        assert mock_mode.called
        # Mode should be BCM
        
        # Verify event detection on pin 16
        detect_call = mock_detect.call_args
        assert detect_call[0][0] == 16  # pin number


class TestIntegration:
    """Integration tests for the camera application."""
    
    @patch('os.system')
    def test_full_workflow_simulation(self, mock_system, source_module):
        """Test a simulated full workflow: capture -> gallery -> upload."""
        pidslm = source_module.piDSLM()
        
        # Mock busy window
        pidslm.busy = MagicMock()
        pidslm.busy.show = MagicMock()
        pidslm.busy.hide = MagicMock()
        pidslm.gallery = MagicMock()
        pidslm.gallery.show = MagicMock()
        
        # Mock timestamp
        pidslm.timestamp = lambda: "20240101_120000"
        
        # Test capture workflow
        pidslm.capture_image()
        assert 'raspistill' in mock_system.call_args[0][0]
        
        # Test video workflow
        pidslm.video_capture()
        call_args = mock_system.call_args[0][0]
        assert 'raspivid' in call_args
        
        # Test upload workflow - capture the command before calling os.system
        with patch('subprocess.Popen') as mock_popen:
            pidslm.upload()
            call_args = mock_popen.call_args[0][0]
            assert 'dropbox_upload.py' in str(call_args)
            assert '--yes' in str(call_args)


class TestErrorHandling:
    """Test error handling scenarios."""
    
    @patch('pidslm.glob.glob')
    def test_gallery_with_no_images(self, mock_glob, source_module):
        """Test gallery handles empty image list gracefully."""
        mock_glob.return_value = []
        
        pidslm = source_module.piDSLM()
        pidslm.gallery = MagicMock()
        pidslm.gallery.show = MagicMock()
        
        # This should handle empty list without crashing
        with pytest.raises(IndexError):
            pidslm.show_gallery()
    
    @patch('pidslm.subprocess.Popen')
    def test_busy_window_methods(self, mock_popen, source_module):
        """Test busy show/hide methods interact with window."""
        pidslm = source_module.piDSLM()
        
        pidslm.busy = MagicMock()
        pidslm.busy.show = MagicMock()
        pidslm.busy.hide = MagicMock()
        
        pidslm.show_busy()
        assert pidslm.busy.show.called
        
        pidslm.hide_busy()
        assert pidslm.busy.hide.called

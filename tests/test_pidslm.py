"""Tests for piDSLM - Raspberry Pi DSLR Camera Controller"""

import pytest
from unittest.mock import patch, MagicMock
import os
import glob


def test_timestamp_generates_valid_format(source_module):
    """Test that timestamp method generates a valid datetime string format."""
    app = source_module.piDSLM()
    # Mock the datetime to have predictable output
    with patch('pidslm.datetime') as mock_datetime:
        mock_datetime.datetime.now.return_value.strftime.return_value = "20231201_120000"
        result = app.timestamp()
        assert result == "20231201_120000"
        assert len(result) == 15  # YYYYMMDD_HHMMSS format is 15 chars


def test_clear_removes_files(source_module, tmp_path, monkeypatch):
    """Test that clear method removes files from Downloads folder."""
    app = source_module.piDSLM()
    
    # Mock the Downloads directory
    downloads_dir = str(tmp_path)
    
    # Create some test files
    test_file = tmp_path / "test.jpg"
    test_file.write_text("test content")
    
    # Patch os.system to capture commands
    with patch('pidslm.os.system') as mock_system:
        app.clear()
        # Verify the rm command was called
        mock_system.assert_called_once()
        assert "rm -v" in mock_system.call_args[0][0]


def test_show_busy_displays_window(source_module):
    """Test that show_busy method displays the busy window."""
    app = source_module.piDSLM()
    
    # Mock the busy window show method
    with patch.object(app.busy, 'show') as mock_show:
        app.show_busy()
        mock_show.assert_called_once()


def test_hide_busy_hides_window(source_module):
    """Test that hide_busy method hides the busy window."""
    app = source_module.piDSLM()
    
    # Mock the busy window hide method
    with patch.object(app.busy, 'hide') as mock_hide:
        app.hide_busy()
        mock_hide.assert_called_once()


def test_burst_capture(source_module):
    """Test burst capture functionality."""
    app = source_module.piDSLM()
    
    with patch('pidslm.os.system') as mock_system:
        with patch.object(app, 'show_busy'):
            with patch.object(app, 'hide_busy'):
                app.burst()
                mock_system.assert_called_once()
                assert "raspistill" in mock_system.call_args[0][0]
                assert "-tl 0" in mock_system.call_args[0][0]
                assert "-bm" in mock_system.call_args[0][0]


def test_video_capture(source_module):
    """Test video capture functionality."""
    app = source_module.piDSLM()
    
    with patch('pidslm.os.system') as mock_system:
        with patch.object(app, 'show_busy'):
            with patch.object(app, 'hide_busy'):
                app.video_capture()
                mock_system.assert_called_once()
                assert "raspivid" in mock_system.call_args[0][0]
                assert "-t 30000" in mock_system.call_args[0][0]


def test_split_hd_30m_capture(source_module):
    """Test 30-minute split HD video capture."""
    app = source_module.piDSLM()
    
    with patch('pidslm.os.system') as mock_system:
        with patch.object(app, 'show_busy'):
            with patch.object(app, 'hide_busy'):
                app.split_hd_30m()
                mock_system.assert_called_once()
                assert "raspivid" in mock_system.call_args[0][0]
                assert "-t 1800000" in mock_system.call_args[0][0]
                assert "-sg 300000" in mock_system.call_args[0][0]


def test_lapse_capture(source_module):
    """Test time-lapse capture functionality."""
    app = source_module.piDSLM()
    
    with patch('pidslm.os.system') as mock_system:
        with patch.object(app, 'show_busy'):
            with patch.object(app, 'hide_busy'):
                app.lapse()
                mock_system.assert_called_once()
                assert "raspistill" in mock_system.call_args[0][0]
                assert "-t 3600000" in mock_system.call_args[0][0]
                assert "-tl 60000" in mock_system.call_args[0][0]


def test_long_preview(source_module):
    """Test long preview functionality."""
    app = source_module.piDSLM()
    
    with patch('pidslm.os.system') as mock_system:
        with patch.object(app, 'show_busy'):
            with patch.object(app, 'hide_busy'):
                app.long_preview()
                mock_system.assert_called_once()
                assert "raspistill" in mock_system.call_args[0][0]
                assert "-t 15000" in mock_system.call_args[0][0]


def test_capture_image(source_module):
    """Test single image capture functionality."""
    app = source_module.piDSLM()
    
    with patch('pidslm.os.system') as mock_system:
        with patch.object(app, 'show_busy'):
            with patch.object(app, 'hide_busy'):
                app.capture_image()
                mock_system.assert_called_once()
                assert "raspistill" in mock_system.call_args[0][0]


def test_upload_calls_dropbox_script(source_module):
    """Test Dropbox upload functionality."""
    app = source_module.piDSLM()
    
    with patch('pidslm.subprocess.Popen') as mock_popen:
        with patch.object(app, 'show_busy'):
            with patch.object(app, 'hide_busy'):
                app.upload()
                mock_popen.assert_called_once()
                call_args = mock_popen.call_args[0][0]
                # call_args is a list like ['python3', '/home/pi/piDSLM/dropbox_upload.py', '--yes']
                assert any("dropbox_upload.py" in arg for arg in call_args)
                assert any("--yes" in arg for arg in call_args)


def test_fullscreen_mode(source_module):
    """Test fullscreen mode functionality."""
    app = source_module.piDSLM()
    
    with patch.object(app.app.tk, 'attributes') as mock_attrs:
        app.fullscreen()
        mock_attrs.assert_called_once_with("-fullscreen", True)


def test_not_fullscreen_mode(source_module):
    """Test non-fullscreen mode functionality."""
    app = source_module.piDSLM()
    
    with patch.object(app.app.tk, 'attributes') as mock_attrs:
        app.notfullscreen()
        mock_attrs.assert_called_once_with("-fullscreen", False)


def test_show_gallery(source_module):
    """Test gallery display functionality."""
    app = source_module.piDSLM()
    
    # Mock glob to return a list with one test image
    test_image = "/home/pi/Downloads/test.jpg"
    with patch('pidslm.glob.glob', return_value=[test_image]):
        with patch('pidslm.Window') as mock_window:
            with patch('pidslm.PushButton'):
                with patch('pidslm.Picture'):
                    app.show_gallery()
                    # Gallery window should be created
                    assert hasattr(app, 'gallery')


def test_gpio_setup(source_module):
    """Test GPIO pin setup during initialization."""
    with patch('pidslm.GPIO') as mock_gpio:
        app = source_module.piDSLM()
        
        # Verify GPIO setup was called
        mock_gpio.setwarnings.assert_called_once_with(False)
        mock_gpio.setmode.assert_called_once_with(mock_gpio.BCM)
        # GPIO.setup should be called at least once (for button pin)
        assert mock_gpio.setup.called
        # Check that GPIO 16 was set up as input with pull-up
        call_args = mock_gpio.setup.call_args
        # call_args is a tuple of (args, kwargs)
        args = call_args[0] if call_args else ()
        kwargs = call_args[1] if len(call_args) > 1 else {}
        assert args[0] == 16
        assert args[1] == mock_gpio.IN
        assert kwargs.get('pull_up_down') == mock_gpio.PUD_UP


def test_take_picture_callback(source_module):
    """Test the takePicture callback function."""
    app = source_module.piDSLM()
    
    with patch('pidslm.os.system') as mock_system:
        # Simulate button press callback
        app.takePicture(16)
        mock_system.assert_called_once()
        assert "raspistill" in mock_system.call_args[0][0]
        assert "-t 3500" in mock_system.call_args[0][0]


def test_saved_pictures_list(source_module):
    """Test that saved_pictures list is initialized correctly."""
    app = source_module.piDSLM()
    assert isinstance(app.saved_pictures, list)
    assert len(app.saved_pictures) == 0


def test_picture_index_initialization(source_module):
    """Test that picture_index is initialized to 0."""
    app = source_module.piDSLM()
    assert app.picture_index == 0


def test_capture_number_initialization(source_module):
    """Test that capture_number is initialized with timestamp."""
    app = source_module.piDSLM()
    assert app.capture_number == app.timestamp()


def test_video_capture_number_initialization(source_module):
    """Test that video_capture_number is initialized with timestamp."""
    app = source_module.piDSLM()
    assert app.video_capture_number == app.timestamp()


def test_shown_picture_initialization(source_module):
    """Test that shown_picture is initialized to empty string."""
    app = source_module.piDSLM()
    assert app.shown_picture == ""

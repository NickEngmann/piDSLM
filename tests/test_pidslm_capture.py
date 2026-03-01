"""Tests for piDSLM camera capture functionality."""

import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the repo directory to the path
sys.path.insert(0, '')


def test_pidslm_init(source_module):
    """Test that piDSLM app initializes correctly."""
    with patch('pidslm.App') as mock_app:
        with patch('pidslm.GPIO') as mock_gpio:
            app = source_module.piDSLM()
            assert app is not None
            assert hasattr(app, 'app')
            assert hasattr(app, 'busy')


def test_pidslm_timestamp(source_module):
    """Test timestamp generation."""
    with patch('pidslm.App') as mock_app:
        with patch('pidslm.GPIO') as mock_gpio:
            app = source_module.piDSLM()
            timestamp = app.timestamp()
            assert isinstance(timestamp, str)
            assert len(timestamp) == 15  # YYYYMMDD_HHMMSS
            assert '_' in timestamp


def test_pidslm_clear(source_module):
    """Test clear folder functionality."""
    with patch('pidslm.App') as mock_app:
        with patch('pidslm.GPIO') as mock_gpio:
            with patch('pidslm.os.system') as mock_system:
                app = source_module.piDSLM()
                app.clear()
                assert mock_system.called
                assert 'rm -v /home/pi/Downloads/*' in str(mock_system.call_args)


def test_pidslm_show_hide_busy(source_module):
    """Test busy indicator functionality."""
    with patch('pidslm.App') as mock_app:
        with patch('pidslm.GPIO') as mock_gpio:
            app = source_module.piDSLM()
            app.show_busy()
            app.hide_busy()
            assert True


def test_pidslm_burst_mode(source_module):
    """Test burst mode capture."""
    with patch('pidslm.App') as mock_app:
        with patch('pidslm.GPIO') as mock_gpio:
            with patch('pidslm.os.system') as mock_system:
                app = source_module.piDSLM()
                app.burst()
                assert mock_system.called
                assert 'raspistill' in str(mock_system.call_args)
                assert 'BR' in str(mock_system.call_args)


def test_pidslm_lapse_mode(source_module):
    """Test timelapse mode."""
    with patch('pidslm.App') as mock_app:
        with patch('pidslm.GPIO') as mock_gpio:
            with patch('pidslm.os.system') as mock_system:
                app = source_module.piDSLM()
                app.lapse()
                assert mock_system.called
                assert 'raspistill' in str(mock_system.call_args)
                assert 'TL' in str(mock_system.call_args)


def test_pidslm_video_capture(source_module):
    """Test video capture."""
    with patch('pidslm.App') as mock_app:
        with patch('pidslm.GPIO') as mock_gpio:
            with patch('pidslm.os.system') as mock_system:
                app = source_module.piDSLM()
                app.video_capture()
                assert mock_system.called
                assert 'raspivid' in str(mock_system.call_args)


def test_pidslm_long_preview(source_module):
    """Test long preview."""
    with patch('pidslm.App') as mock_app:
        with patch('pidslm.GPIO') as mock_gpio:
            with patch('pidslm.os.system') as mock_system:
                app = source_module.piDSLM()
                app.long_preview()
                assert mock_system.called
                assert 'raspistill' in str(mock_system.call_args)


def test_pidslm_capture_image(source_module):
    """Test image capture."""
    with patch('pidslm.App') as mock_app:
        with patch('pidslm.GPIO') as mock_gpio:
            with patch('pidslm.os.system') as mock_system:
                app = source_module.piDSLM()
                app.capture_image()
                assert mock_system.called
                assert 'raspistill' in str(mock_system.call_args)


def test_pidslm_take_picture(source_module):
    """Test take picture callback."""
    with patch('pidslm.App') as mock_app:
        with patch('pidslm.GPIO') as mock_gpio:
            with patch('pidslm.os.system') as mock_system:
                app = source_module.piDSLM()
                app.takePicture(16)  # channel parameter
                assert mock_system.called
                assert 'raspistill' in str(mock_system.call_args)


def test_pidslm_split_hd_30m(source_module):
    """Test 30 minute video split."""
    with patch('pidslm.App') as mock_app:
        with patch('pidslm.GPIO') as mock_gpio:
            with patch('pidslm.os.system') as mock_system:
                app = source_module.piDSLM()
                app.split_hd_30m()
                assert mock_system.called
                assert 'raspivid' in str(mock_system.call_args)


def test_pidslm_upload(source_module):
    """Test upload to Dropbox."""
    with patch('pidslm.App') as mock_app:
        with patch('pidslm.GPIO') as mock_gpio:
            with patch('pidslm.subprocess') as mock_subprocess:
                app = source_module.piDSLM()
                app.upload()
                assert mock_subprocess.Popen.called
                assert 'dropbox_upload.py' in str(mock_subprocess.Popen.call_args)


def test_pidslm_gpio_setup(source_module):
    """Test GPIO setup."""
    with patch('pidslm.App') as mock_app:
        with patch('pidslm.GPIO') as mock_gpio:
            app = source_module.piDSLM()
            assert mock_gpio.setmode.called
            assert mock_gpio.setup.called
            assert mock_gpio.add_event_detect.called


def test_pidslm_fullscreen(source_module):
    """Test fullscreen functionality."""
    with patch('pidslm.App') as mock_app:
        with patch('pidslm.GPIO') as mock_gpio:
            app = source_module.piDSLM()
            app.fullscreen()
            app.notfullscreen()
            assert True


def test_pidslm_show_gallery(source_module):
    """Test gallery display."""
    with patch('pidslm.App') as mock_app:
        with patch('pidslm.GPIO') as mock_gpio:
            with patch('pidslm.glob') as mock_glob:
                mock_glob.glob.return_value = []
                app = source_module.piDSLM()
                app.show_gallery()
                assert app.gallery is not None


def test_pidslm_picture_navigation(source_module):
    """Test picture navigation in gallery."""
    with patch('pidslm.App') as mock_app:
        with patch('pidslm.GPIO') as mock_gpio:
            with patch('pidslm.glob') as mock_glob:
                mock_glob.glob.return_value = []
                app = source_module.piDSLM()
                app.show_gallery()
                # Test picture navigation methods exist
                assert hasattr(app, 'picture_left')
                assert hasattr(app, 'picture_right')


def test_pidslm_capture_number(source_module):
    """Test capture number initialization."""
    with patch('pidslm.App') as mock_app:
        with patch('pidslm.GPIO') as mock_gpio:
            app = source_module.piDSLM()
            assert hasattr(app, 'capture_number')
            assert isinstance(app.capture_number, str)


def test_pidslm_saved_pictures(source_module):
    """Test saved pictures list."""
    with patch('pidslm.App') as mock_app:
        with patch('pidslm.GPIO') as mock_gpio:
            app = source_module.piDSLM()
            assert hasattr(app, 'saved_pictures')
            assert isinstance(app.saved_pictures, list)


def test_pidslm_picture_index(source_module):
    """Test picture index."""
    with patch('pidslm.App') as mock_app:
        with patch('pidslm.GPIO') as mock_gpio:
            app = source_module.piDSLM()
            assert hasattr(app, 'picture_index')
            assert app.picture_index == 0

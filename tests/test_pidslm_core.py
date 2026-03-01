"""Tests for piDSLM core functionality."""

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


def test_pidslm_capture_mode(source_module):
    """Test capture mode functionality."""
    with patch('pidslm.App') as mock_app:
        with patch('pidslm.GPIO') as mock_gpio:
            app = source_module.piDSLM()
            # Test that capture mode is initialized
            assert hasattr(app, 'capture_mode')
            assert app.capture_mode in ['single', 'burst', 'interval']


def test_pidslm_shutter_button(source_module):
    """Test shutter button callback."""
    with patch('pidslm.App') as mock_app:
        with patch('pidslm.GPIO') as mock_gpio:
            with patch('pidslm.subprocess') as mock_subprocess:
                app = source_module.piDSLM()
                # Simulate shutter button press
                app.shutter_button_callback()
                # Check that camera command was called
                assert mock_subprocess.Popen.called


def test_pidslm_burst_mode(source_module):
    """Test burst mode functionality."""
    with patch('pidslm.App') as mock_app:
        with patch('pidslm.GPIO') as mock_gpio:
            app = source_module.piDSLM()
            # Test burst mode setting
            app.set_burst_mode()
            assert app.capture_mode == 'burst'


def test_pidslm_interval_mode(source_module):
    """Test interval mode functionality."""
    with patch('pidslm.App') as mock_app:
        with patch('pidslm.GPIO') as mock_gpio:
            app = source_module.piDSLM()
            # Test interval mode setting
            app.set_interval_mode()
            assert app.capture_mode == 'interval'


def test_pidslm_single_mode(source_module):
    """Test single mode functionality."""
    with patch('pidslm.App') as mock_app:
        with patch('pidslm.GPIO') as mock_gpio:
            app = source_module.piDSLM()
            # Test single mode setting
            app.set_single_mode()
            assert app.capture_mode == 'single'


def test_pidslm_busy_indicator(source_module):
    """Test busy indicator functionality."""
    with patch('pidslm.App') as mock_app:
        with patch('pidslm.GPIO') as mock_gpio:
            app = source_module.piDSLM()
            # Test busy indicator methods
            app.show_busy()
            app.hide_busy()
            # Just verify methods exist and can be called
            assert True


def test_pidslm_cleanup(source_module):
    """Test cleanup functionality."""
    with patch('pidslm.App') as mock_app:
        with patch('pidslm.GPIO') as mock_gpio:
            app = source_module.piDSLM()
            # Test cleanup method
            app.cleanup()
            # Verify GPIO cleanup was called
            assert mock_gpio.cleanup.called


def test_pidslm_gpio_setup(source_module):
    """Test GPIO pin setup."""
    with patch('pidslm.App') as mock_app:
        with patch('pidslm.GPIO') as mock_gpio:
            app = source_module.piDSLM()
            # Verify GPIO mode was set
            assert mock_gpio.setmode.called


def test_pidslm_run_method(source_module):
    """Test run method."""
    with patch('pidslm.App') as mock_app:
        with patch('pidslm.GPIO') as mock_gpio:
            app = source_module.piDSLM()
            # Mock the app.run() method
            app.app.run = MagicMock()
            app.run()
            assert app.app.run.called


def test_pidslm_filename_generation(source_module):
    """Test filename generation."""
    with patch('pidslm.App') as mock_app:
        with patch('pidslm.GPIO') as mock_gpio:
            app = source_module.piDSLM()
            filename = app.generate_filename()
            assert filename.endswith('.jpg')


def test_pidslm_datetime_format(source_module):
    """Test datetime formatting."""
    with patch('pidslm.App') as mock_app:
        with patch('pidslm.GPIO') as mock_gpio:
            app = source_module.piDSLM()
            dt = app.get_datetime_string()
            assert len(dt) == 15
            assert '_' in dt


def test_pidslm_process_image(source_module):
    """Test image processing."""
    with patch('pidslm.App') as mock_app:
        with patch('pidslm.GPIO') as mock_gpio:
            with patch('pidslm.subprocess') as mock_subprocess:
                app = source_module.piDSLM()
                mock_subprocess.Popen.return_value = MagicMock()
                result = app.process_image('test.jpg')
                assert mock_subprocess.Popen.called


def test_pidslm_show_preview(source_module):
    """Test preview display."""
    with patch('pidslm.App') as mock_app:
        with patch('pidslm.GPIO') as mock_gpio:
            app = source_module.piDSLM()
            mock_picture = MagicMock()
            app.preview = mock_picture
            app.show_preview('/tmp/test.jpg')
            assert mock_picture.value == '/tmp/test.jpg'


def test_pidslm_cleanup_temp_files(source_module):
    """Test temp file cleanup."""
    with patch('pidslm.App') as mock_app:
        with patch('pidslm.GPIO') as mock_gpio:
            app = source_module.piDSLM()
            result = app.cleanup_temp_files()
            assert result is not None


def test_pidslm_set_capture_mode(source_module):
    """Test setting capture mode."""
    with patch('pidslm.App') as mock_app:
        with patch('pidslm.GPIO') as mock_gpio:
            app = source_module.piDSLM()
            app.set_single_mode()
            assert app.capture_mode == 'single'
            app.set_burst_mode()
            assert app.capture_mode == 'burst'
            app.set_interval_mode()
            assert app.capture_mode == 'interval'


def test_pidslm_upload_to_dropbox(source_module):
    """Test Dropbox upload."""
    with patch('pidslm.App') as mock_app:
        with patch('pidslm.GPIO') as mock_gpio:
            with patch('pidslm.subprocess') as mock_subprocess:
                app = source_module.piDSLM()
                app.upload_to_dropbox()
                assert mock_subprocess.Popen.called


def test_pidslm_gpio_interrupts(source_module):
    """Test GPIO interrupt setup."""
    with patch('pidslm.App') as mock_app:
        with patch('pidslm.GPIO') as mock_gpio:
            app = source_module.piDSLM()
            assert mock_gpio.add_event_detect.called


def test_pidslm_button_callbacks(source_module):
    """Test button callback setup."""
    with patch('pidslm.App') as mock_app:
        with patch('pidslm.GPIO') as mock_gpio:
            app = source_module.piDSLM()
            # Test that button callbacks are defined
            assert hasattr(app, 'set_single_mode')
            assert hasattr(app, 'set_burst_mode')
            assert hasattr(app, 'set_interval_mode')
            assert hasattr(app, 'shutter_button_callback')

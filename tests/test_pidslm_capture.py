"""Tests for piDSLM capture functionality"""

import pytest
from unittest.mock import patch, MagicMock
from guizero import App, PushButton, Text, Picture, Window


class TestPiDSLMCapture:
    """Test cases for capture operations"""

    def test_burst_capture(self, source_module):
        """Test burst capture functionality"""
        with patch('pidslm.App') as mock_app:
            with patch('pidslm.GPIO') as mock_gpio:
                with patch('pidslm.os') as mock_os:
                    mock_app.return_value.window = MagicMock()
                    mock_app.return_value.tk = MagicMock()
                    
                    instance = source_module.piDSLM()
                    instance.show_busy = MagicMock()
                    instance.hide_busy = MagicMock()
                    
                    instance.burst()
                    
                    assert instance.show_busy.called
                    assert mock_os.system.called
                    assert 'raspistill' in str(mock_os.system.call_args)
                    assert instance.hide_busy.called

    def test_split_hd_30m(self, source_module):
        """Test 30 minute HD video split functionality"""
        with patch('pidslm.App') as mock_app:
            with patch('pidslm.GPIO') as mock_gpio:
                with patch('pidslm.os') as mock_os:
                    mock_app.return_value.window = MagicMock()
                    mock_app.return_value.tk = MagicMock()
                    
                    instance = source_module.piDSLM()
                    instance.show_busy = MagicMock()
                    instance.hide_busy = MagicMock()
                    
                    instance.split_hd_30m()
                    
                    assert instance.show_busy.called
                    assert mock_os.system.called
                    assert 'raspivid' in str(mock_os.system.call_args)
                    assert instance.hide_busy.called

    def test_lapse_capture(self, source_module):
        """Test time-lapse capture functionality"""
        with patch('pidslm.App') as mock_app:
            with patch('pidslm.GPIO') as mock_gpio:
                with patch('pidslm.os') as mock_os:
                    mock_app.return_value.window = MagicMock()
                    mock_app.return_value.tk = MagicMock()
                    
                    instance = source_module.piDSLM()
                    instance.show_busy = MagicMock()
                    instance.hide_busy = MagicMock()
                    
                    instance.lapse()
                    
                    assert instance.show_busy.called
                    assert mock_os.system.called
                    assert 'raspistill' in str(mock_os.system.call_args)
                    assert instance.hide_busy.called

    def test_long_preview(self, source_module):
        """Test long preview functionality"""
        with patch('pidslm.App') as mock_app:
            with patch('pidslm.GPIO') as mock_gpio:
                with patch('pidslm.os') as mock_os:
                    mock_app.return_value.window = MagicMock()
                    mock_app.return_value.tk = MagicMock()
                    
                    instance = source_module.piDSLM()
                    instance.show_busy = MagicMock()
                    instance.hide_busy = MagicMock()
                    
                    instance.long_preview()
                    
                    assert instance.show_busy.called
                    assert mock_os.system.called
                    assert 'raspistill' in str(mock_os.system.call_args)
                    assert instance.hide_busy.called

    def test_capture_image(self, source_module):
        """Test single image capture functionality"""
        with patch('pidslm.App') as mock_app:
            with patch('pidslm.GPIO') as mock_gpio:
                with patch('pidslm.os') as mock_os:
                    mock_app.return_value.window = MagicMock()
                    mock_app.return_value.tk = MagicMock()
                    
                    instance = source_module.piDSLM()
                    instance.show_busy = MagicMock()
                    instance.hide_busy = MagicMock()
                    
                    instance.capture_image()
                    
                    assert instance.show_busy.called
                    assert mock_os.system.called
                    assert 'raspistill' in str(mock_os.system.call_args)
                    assert instance.hide_busy.called

    def test_take_picture_callback(self, source_module):
        """Test picture taking via GPIO callback"""
        with patch('pidslm.App') as mock_app:
            with patch('pidslm.GPIO') as mock_gpio:
                with patch('pidslm.os') as mock_os:
                    mock_app.return_value.window = MagicMock()
                    mock_app.return_value.tk = MagicMock()
                    
                    instance = source_module.piDSLM()
                    
                    # Simulate GPIO callback
                    instance.takePicture(16)
                    
                    assert mock_os.system.called
                    assert 'raspistill' in str(mock_os.system.call_args)

    def test_video_capture(self, source_module):
        """Test video capture functionality"""
        with patch('pidslm.App') as mock_app:
            with patch('pidslm.GPIO') as mock_gpio:
                with patch('pidslm.os') as mock_os:
                    mock_app.return_value.window = MagicMock()
                    mock_app.return_value.tk = MagicMock()
                    
                    instance = source_module.piDSLM()
                    instance.show_busy = MagicMock()
                    instance.hide_busy = MagicMock()
                    
                    instance.video_capture()
                    
                    assert instance.show_busy.called
                    assert mock_os.system.called
                    assert 'raspivid' in str(mock_os.system.call_args)
                    assert instance.hide_busy.called

    def test_clear_folder(self, source_module):
        """Test clear folder functionality"""
        with patch('pidslm.App') as mock_app:
            with patch('pidslm.GPIO') as mock_gpio:
                with patch('pidslm.os') as mock_os:
                    mock_app.return_value.window = MagicMock()
                    mock_app.return_value.tk = MagicMock()
                    
                    instance = source_module.piDSLM()
                    instance.show_busy = MagicMock()
                    instance.hide_busy = MagicMock()
                    
                    instance.clear()
                    
                    assert instance.show_busy.called
                    assert mock_os.system.called
                    assert 'rm -v /home/pi/Downloads/*' in str(mock_os.system.call_args)
                    assert instance.hide_busy.called

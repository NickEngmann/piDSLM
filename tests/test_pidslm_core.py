"""Tests for piDSLM core functionality"""

import pytest
from unittest.mock import patch, MagicMock
from guizero import App, PushButton, Text, Picture, Window


class TestPiDSLMInitialization:
    """Test cases for piDSLM initialization"""

    def test_app_initialization(self, source_module):
        """Test that the app initializes correctly"""
        with patch('pidslm.App') as mock_app:
            with patch('pidslm.GPIO') as mock_gpio:
                mock_app_instance = MagicMock()
                mock_app.return_value = mock_app_instance
                mock_app_instance.window = MagicMock()
                mock_app_instance.tk = MagicMock()
                mock_app_instance.display = MagicMock()
                
                instance = source_module.piDSLM()
                assert instance is not None
                assert hasattr(instance, 'capture_number')
                assert hasattr(instance, 'video_capture_number')
                assert hasattr(instance, 'picture_index')
                assert hasattr(instance, 'saved_pictures')

    def test_timestamp_generation(self, source_module):
        """Test timestamp generation for file naming"""
        with patch('pidslm.App') as mock_app:
            with patch('pidslm.GPIO') as mock_gpio:
                mock_app.return_value.window = MagicMock()
                mock_app.return_value.tk = MagicMock()
                
                instance = source_module.piDSLM()
                timestamp = instance.timestamp()
                
                # Verify timestamp format: YYYYMMDD_HHMMSS
                assert len(timestamp) == 16
                assert '_' in timestamp

    def test_show_busy(self, source_module):
        """Test showing busy indicator"""
        with patch('pidslm.App') as mock_app:
            with patch('pidslm.GPIO') as mock_gpio:
                mock_app.return_value.window = MagicMock()
                mock_app.return_value.tk = MagicMock()
                
                instance = source_module.piDSLM()
                instance.busy = MagicMock()
                instance.busy.show = MagicMock()
                
                instance.show_busy()
                
                assert instance.busy.show.called

    def test_hide_busy(self, source_module):
        """Test hiding busy indicator"""
        with patch('pidslm.App') as mock_app:
            with patch('pidslm.GPIO') as mock_gpio:
                mock_app.return_value.window = MagicMock()
                mock_app.return_value.tk = MagicMock()
                
                instance = source_module.piDSLM()
                instance.busy = MagicMock()
                instance.busy.hide = MagicMock()
                
                instance.hide_busy()
                
                assert instance.busy.hide.called

    def test_fullscreen_functions(self, source_module):
        """Test fullscreen toggle functions"""
        with patch('pidslm.App') as mock_app:
            with patch('pidslm.GPIO') as mock_gpio:
                mock_app_instance = MagicMock()
                mock_app.return_value = mock_app_instance
                mock_app_instance.tk = MagicMock()
                
                instance = source_module.piDSLM()
                
                instance.fullscreen()
                assert mock_app_instance.tk.attributes.called
                
                instance.notfullscreen()
                assert mock_app_instance.tk.attributes.called

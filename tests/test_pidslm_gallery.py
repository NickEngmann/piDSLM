"""Tests for piDSLM gallery and upload functionality"""

import pytest
from unittest.mock import patch, MagicMock
from guizero import App, PushButton, Text, Picture, Window


class TestPiDSLMGallery:
    """Test cases for gallery functionality"""

    def test_show_gallery(self, source_module):
        """Test gallery viewing functionality"""
        with patch('pidslm.App') as mock_app:
            with patch('pidslm.GPIO') as mock_gpio:
                with patch('pidslm.glob') as mock_glob:
                    with patch('pidslm.Window') as mock_window:
                        with patch('pidslm.PushButton') as mock_button:
                            with patch('pidslm.Picture') as mock_picture:
                                mock_app.return_value.window = MagicMock()
                                mock_app.return_value.tk = MagicMock()
                                
                                instance = source_module.piDSLM()
                                
                                # Mock glob to return some test files
                                mock_glob.glob.return_value = [
                                    '/home/pi/Downloads/img_001.jpg',
                                    '/home/pi/Downloads/img_002.jpg'
                                ]
                                
                                instance.show_gallery()
                                
                                # Verify glob was called for image files
                                assert mock_glob.glob.called
                                assert 'Downloads/*.jpg' in str(mock_glob.glob.call_args)

    def test_picture_navigation(self, source_module):
        """Test picture navigation in gallery"""
        with patch('pidslm.App') as mock_app:
            with patch('pidslm.GPIO') as mock_gpio:
                with patch('pidslm.glob') as mock_glob:
                    with patch('pidslm.Window') as mock_window:
                        with patch('pidslm.PushButton') as mock_button:
                            with patch('pidslm.Picture') as mock_picture:
                                mock_app.return_value.window = MagicMock()
                                mock_app.return_value.tk = MagicMock()
                                
                                instance = source_module.piDSLM()
                                
                                # Mock glob to return some test files
                                mock_glob.glob.return_value = [
                                    '/home/pi/Downloads/img_001.jpg',
                                    '/home/pi/Downloads/img_002.jpg',
                                    '/home/pi/Downloads/img_003.jpg'
                                ]
                                instance.show_gallery()
                                
                                # Test picture_left
                                initial_index = instance.picture_index
                                instance.picture_left()
                                assert instance.picture_index == initial_index - 1
                                
                                # Test picture_right
                                initial_index = instance.picture_index
                                instance.picture_right()
                                assert instance.picture_index == initial_index + 1


class TestPiDSLMUpload:
    """Test cases for upload functionality"""

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
                    
                    instance.upload()
                    
                    assert instance.show_busy.called
                    assert mock_subprocess.Popen.called
                    call_args = str(mock_subprocess.Popen.call_args)
                    assert 'dropbox_upload.py' in call_args
                    assert '--yes' in call_args
                    assert instance.hide_busy.called


class TestPiDSLMIntegration:
    """Integration tests for piDSLM"""

    def test_full_workflow(self, source_module):
        """Test a complete workflow: capture, view gallery"""
        with patch('pidslm.App') as mock_app:
            with patch('pidslm.GPIO') as mock_gpio:
                with patch('pidslm.os') as mock_os:
                    with patch('pidslm.glob') as mock_glob:
                        mock_app.return_value.window = MagicMock()
                        mock_app.return_value.tk = MagicMock()
                        mock_glob.glob.return_value = []
                        
                        instance = source_module.piDSLM()
                        
                        # Capture image
                        instance.capture_image()
                        assert mock_os.system.called
                        
                        # Show gallery
                        instance.show_gallery()
                        assert mock_glob.glob.called

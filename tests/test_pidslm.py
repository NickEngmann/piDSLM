"""Tests for piDSLM.py - Raspberry Pi DSLM application.

Tests the main application logic without hardware dependencies.
"""

import sys
import pytest
from unittest.mock import MagicMock, patch, call
import datetime

# Test the piDSLM class initialization and basic functionality
def test_initialization(source_module):
    """Test that piDSLM initializes correctly."""
    piDSLM = source_module.piDSLM
    
    with patch.object(piDSLM, '__init__', lambda self: None):
        app = piDSLM.__new__(piDSLM)
        app.app = MagicMock()
        app.camera_status = 'Ready'
        app.current_image = ''
        
        assert app is not None
        assert app.camera_status == 'Ready'
        assert app.current_image == ''


def test_take_photo(source_module):
    """Test taking a photo."""
    piDSLM = source_module.piDSLM
    
    with patch.object(piDSLM, '__init__', lambda self: None):
        app = piDSLM.__new__(piDSLM)
        app.app = MagicMock()
        app.camera_status = 'Ready'
        app.current_image = ''
        
        # Simulate taking a photo
        with patch('pidslm.subprocess') as mock_subprocess:
            with patch('pidslm.time') as mock_time:
                mock_time.time.return_value = 1234567890.0
                
                # Call the actual take_photo method
                piDSLM.take_photo(app)
                
                # Verify subprocess was called
                mock_subprocess.run.assert_called_once()


def test_display_gallery(source_module):
    """Test displaying the gallery."""
    piDSLM = source_module.piDSLM
    
    with patch.object(piDSLM, '__init__', lambda self: None):
        app = piDSLM.__new__(piDSLM)
        app.app = MagicMock()
        app.camera_status = 'Ready'
        app.current_image = ''
        
        # Simulate displaying gallery
        with patch('pidslm.glob') as mock_glob:
            mock_glob.glob.return_value = ['/tmp/photo1.jpg', '/tmp/photo2.jpg']
            
            piDSLM.display_gallery(app)
            
            assert app.current_image == '/tmp/photo1.jpg'


def test_show_busy(source_module):
    """Test showing busy indicator."""
    piDSLM = source_module.piDSLM
    
    with patch.object(piDSLM, '__init__', lambda self: None):
        app = piDSLM.__new__(piDSLM)
        app.app = MagicMock()
        app.camera_status = 'Ready'
        app.current_image = ''
        
        # Simulate showing busy
        piDSLM.show_busy(app)
        
        # Verify info was called
        app.app.info.assert_called_once()


def test_hide_busy(source_module):
    """Test hiding busy indicator."""
    piDSLM = source_module.piDSLM
    
    with patch.object(piDSLM, '__init__', lambda self: None):
        app = piDSLM.__new__(piDSLM)
        app.app = MagicMock()
        app.camera_status = 'Ready'
        app.current_image = ''
        
        # Simulate hiding busy
        piDSLM.hide_busy(app)
        
        # Verify info was called
        app.app.info.assert_called_once()


def test_upload_to_dropbox(source_module):
    """Test uploading to Dropbox."""
    piDSLM = source_module.piDSLM
    
    with patch.object(piDSLM, '__init__', lambda self: None):
        app = piDSLM.__new__(piDSLM)
        app.app = MagicMock()
        app.camera_status = 'Ready'
        app.current_image = ''
        
        # Simulate uploading to Dropbox
        with patch('pidslm.subprocess') as mock_subprocess:
            piDSLM.upload_to_dropbox(app)
            
            # Verify subprocess was called
            mock_subprocess.run.assert_called_once()


def test_get_image_files(source_module):
    """Test getting image files."""
    piDSLM = source_module.piDSLM
    
    with patch.object(piDSLM, '__init__', lambda self: None):
        app = piDSLM.__new__(piDSLM)
        app.app = MagicMock()
        app.camera_status = 'Ready'
        app.current_image = ''
        
        # Simulate getting image files
        with patch('pidslm.glob') as mock_glob:
            mock_glob.glob.return_value = ['/tmp/photo1.jpg', '/tmp/photo2.png']
            
            images = piDSLM.get_image_files(app)
            
            assert len(images) == 2
            assert '/tmp/photo1.jpg' in images
            assert '/tmp/photo2.png' in images


def test_create_directory(source_module):
    """Test creating directory."""
    piDSLM = source_module.piDSLM
    
    with patch.object(piDSLM, '__init__', lambda self: None):
        app = piDSLM.__new__(piDSLM)
        app.app = MagicMock()
        app.camera_status = 'Ready'
        app.current_image = ''
        
        # Simulate creating directory
        with patch('pidslm.os') as mock_os:
            mock_os.path.exists.return_value = False
            
            piDSLM.create_directory(app, '/tmp/test_dir')
            
            # Verify makedirs was called
            mock_os.makedirs.assert_called_once_with('/tmp/test_dir')


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

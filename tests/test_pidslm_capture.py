"""Tests for pidslm.py capture functionality."""

import pytest
import sys
import os
from unittest.mock import patch, MagicMock, call

# Add the repo directory to the path
sys.path.insert(0, '')


def test_clear():
    """Test clear folder functionality."""
    with patch('guizero.App'):
        with patch('guizero.PushButton'):
            with patch('guizero.Text'):
                with patch('guizero.Picture'):
                    with patch('guizero.Window'):
                        with patch('RPi.GPIO'):
                            with patch('pidslm.os.system') as mock_system:
                                import pidslm
                                app = pidslm.piDSLM()
                                
                                with patch.object(app, 'show_busy'):
                                    with patch.object(app, 'hide_busy'):
                                        app.clear()
                                        
                                        # Verify os.system was called with rm command
                                        assert mock_system.called
                                        call_args = mock_system.call_args[0][0]
                                        assert 'rm' in call_args
                                        assert 'Downloads' in call_args


def test_burst():
    """Test burst capture functionality."""
    with patch('guizero.App'):
        with patch('guizero.PushButton'):
            with patch('guizero.Text'):
                with patch('guizero.Picture'):
                    with patch('guizero.Window'):
                        with patch('RPi.GPIO'):
                            with patch('pidslm.os.system') as mock_system:
                                import pidslm
                                app = pidslm.piDSLM()
                                
                                with patch.object(app, 'show_busy'):
                                    with patch.object(app, 'hide_busy'):
                                        app.burst()
                                        
                                        # Verify raspistill command was called
                                        assert mock_system.called
                                        call_args = mock_system.call_args[0][0]
                                        assert 'raspistill' in call_args
                                        assert 'BR' in call_args


def test_split_hd_30m():
    """Test 30 minute split video capture functionality."""
    with patch('guizero.App'):
        with patch('guizero.PushButton'):
            with patch('guizero.Text'):
                with patch('guizero.Picture'):
                    with patch('guizero.Window'):
                        with patch('RPi.GPIO'):
                            with patch('pidslm.os.system') as mock_system:
                                import pidslm
                                app = pidslm.piDSLM()
                                
                                with patch.object(app, 'show_busy'):
                                    with patch.object(app, 'hide_busy'):
                                        app.split_hd_30m()
                                        
                                        # Verify raspivid command was called
                                        assert mock_system.called
                                        call_args = mock_system.call_args[0][0]
                                        assert 'raspivid' in call_args
                                        assert '1800000' in call_args  # 30 minutes in ms


def test_lapse():
    """Test timelapse capture functionality."""
    with patch('guizero.App'):
        with patch('guizero.PushButton'):
            with patch('guizero.Text'):
                with patch('guizero.Picture'):
                    with patch('guizero.Window'):
                        with patch('RPi.GPIO'):
                            with patch('pidslm.os.system') as mock_system:
                                import pidslm
                                app = pidslm.piDSLM()
                                
                                with patch.object(app, 'show_busy'):
                                    with patch.object(app, 'hide_busy'):
                                        app.lapse()
                                        
                                        # Verify raspistill timelapse command was called
                                        assert mock_system.called
                                        call_args = mock_system.call_args[0][0]
                                        assert 'raspistill' in call_args
                                        assert '3600000' in call_args  # 1 hour in ms
                                        assert '60000' in call_args  # 60 second interval


def test_long_preview():
    """Test long preview functionality."""
    with patch('guizero.App'):
        with patch('guizero.PushButton'):
            with patch('guizero.Text'):
                with patch('guizero.Picture'):
                    with patch('guizero.Window'):
                        with patch('RPi.GPIO'):
                            with patch('pidslm.os.system') as mock_system:
                                import pidslm
                                app = pidslm.piDSLM()
                                
                                with patch.object(app, 'show_busy'):
                                    with patch.object(app, 'hide_busy'):
                                        app.long_preview()
                                        
                                        # Verify raspistill command with 15s preview
                                        assert mock_system.called
                                        call_args = mock_system.call_args[0][0]
                                        assert 'raspistill' in call_args
                                        assert '15000' in call_args  # 15 seconds in ms


def test_capture_image():
    """Test single image capture functionality."""
    with patch('guizero.App'):
        with patch('guizero.PushButton'):
            with patch('guizero.Text'):
                with patch('guizero.Picture'):
                    with patch('guizero.Window'):
                        with patch('RPi.GPIO'):
                            with patch('pidslm.os.system') as mock_system:
                                import pidslm
                                app = pidslm.piDSLM()
                                
                                with patch.object(app, 'show_busy'):
                                    with patch.object(app, 'hide_busy'):
                                        app.capture_image()
                                        
                                        # Verify raspistill command was called
                                        assert mock_system.called
                                        call_args = mock_system.call_args[0][0]
                                        assert 'raspistill' in call_args
                                        assert 'cam.jpg' in call_args


def test_takePicture():
    """Test picture taking via GPIO callback."""
    with patch('guizero.App'):
        with patch('guizero.PushButton'):
            with patch('guizero.Text'):
                with patch('guizero.Picture'):
                    with patch('guizero.Window'):
                        with patch('RPi.GPIO'):
                            with patch('pidslm.os.system') as mock_system:
                                import pidslm
                                app = pidslm.piDSLM()
                                
                                with patch('builtins.print'):
                                    app.takePicture(16)  # Pass channel argument
                                    
                                    # Verify raspistill command was called
                                    assert mock_system.called
                                    call_args = mock_system.call_args[0][0]
                                    assert 'raspistill' in call_args
                                    assert 'cam.jpg' in call_args
                                    assert '3500' in call_args  # 3.5 second preview


def test_video_capture():
    """Test video capture functionality."""
    with patch('guizero.App'):
        with patch('guizero.PushButton'):
            with patch('guizero.Text'):
                with patch('guizero.Picture'):
                    with patch('guizero.Window'):
                        with patch('RPi.GPIO'):
                            with patch('pidslm.os.system') as mock_system:
                                import pidslm
                                app = pidslm.piDSLM()
                                
                                with patch.object(app, 'show_busy'):
                                    with patch.object(app, 'hide_busy'):
                                        app.video_capture()
                                        
                                        # Verify raspivid command was called
                                        assert mock_system.called
                                        call_args = mock_system.call_args[0][0]
                                        assert 'raspivid' in call_args
                                        assert '30000' in call_args  # 30 seconds in ms


def test_upload():
    """Test upload to Dropbox functionality."""
    with patch('guizero.App'):
        with patch('guizero.PushButton'):
            with patch('guizero.Text'):
                with patch('guizero.Picture'):
                    with patch('guizero.Window'):
                        with patch('RPi.GPIO'):
                            with patch('pidslm.subprocess.Popen') as mock_popen:
                                import pidslm
                                app = pidslm.piDSLM()
                                
                                with patch.object(app, 'show_busy'):
                                    with patch.object(app, 'hide_busy'):
                                        app.upload()
                                        
                                        # Verify dropbox_upload.py was called
                                        assert mock_popen.called
                                        call_args = mock_popen.call_args[0][0]
                                        # Check that dropbox_upload.py is in the command
                                        assert any('dropbox_upload.py' in str(arg) for arg in call_args)
                                        assert '--yes' in call_args


def test_show_gallery():
    """Test gallery display functionality."""
    with patch('guizero.App'):
        with patch('guizero.PushButton'):
            with patch('guizero.Text'):
                with patch('guizero.Picture'):
                    with patch('guizero.Window'):
                        with patch('RPi.GPIO'):
                            with patch('pidslm.glob.glob') as mock_glob:
                                import pidslm
                                app = pidslm.piDSLM()
                                
                                # Mock saved pictures
                                mock_glob.return_value = ['/home/pi/Downloads/test1.jpg']
                                
                                with patch.object(app, 'show_busy'):
                                    with patch.object(app, 'hide_busy'):
                                        with patch('builtins.print'):
                                            app.show_gallery()
                                            
                                            # Verify glob was called to find images
                                            assert mock_glob.called


def test_fullscreen():
    """Test fullscreen toggle."""
    with patch('guizero.App') as mock_app:
        with patch('guizero.PushButton'):
            with patch('guizero.Text'):
                with patch('guizero.Picture'):
                    with patch('guizero.Window'):
                        with patch('RPi.GPIO'):
                            import pidslm
                            app = pidslm.piDSLM()
                            
                            app.fullscreen()
                            # Verify fullscreen was set
                            assert app.app.tk.attributes.called


def test_notfullscreen():
    """Test not fullscreen toggle."""
    with patch('guizero.App') as mock_app:
        with patch('guizero.PushButton'):
            with patch('guizero.Text'):
                with patch('guizero.Picture'):
                    with patch('guizero.Window'):
                        with patch('RPi.GPIO'):
                            import pidslm
                            app = pidslm.piDSLM()
                            
                            app.notfullscreen()
                            # Verify fullscreen was disabled
                            assert app.app.tk.attributes.called

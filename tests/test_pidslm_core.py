"""Tests for pidslm.py core functionality."""

import pytest
import sys
import os
from unittest.mock import patch, MagicMock, call

# Add the repo directory to the path
sys.path.insert(0, '')


def test_gpio_pin_constants():
    """Test that GPIO pin constants are properly defined."""
    import pidslm
    
    # The module should define these constants
    assert hasattr(pidslm, 'SHUTTER_PIN') or hasattr(pidslm, 'VIDEO_PIN') or hasattr(pidslm, 'BUSY_PIN')


def test_app_initialization():
    """Test that the piDSLM app initializes correctly."""
    with patch('guizero.App') as mock_app:
        with patch('guizero.PushButton'):
            with patch('guizero.Text'):
                with patch('guizero.Picture'):
                    with patch('guizero.Window'):
                        with patch('RPi.GPIO') as mock_gpio:
                            import pidslm
                            app = pidslm.piDSLM()
                            assert app is not None
                            # App should have created the main window
                            assert hasattr(app, 'app')
                            # Verify GPIO was set up
                            assert mock_gpio.setmode.called
                            assert mock_gpio.setup.called


def test_show_busy():
    """Test busy indicator display."""
    with patch('guizero.App'):
        with patch('guizero.PushButton'):
            with patch('guizero.Text'):
                with patch('guizero.Picture'):
                    with patch('guizero.Window') as mock_window:
                        with patch('RPi.GPIO'):
                            import pidslm
                            app = pidslm.piDSLM()
                            
                            # Mock the busy window
                            mock_busy_window = MagicMock()
                            app.busy = mock_busy_window
                            
                            with patch('builtins.print'):
                                app.show_busy()
                                
                                # Verify busy window was shown
                                assert mock_busy_window.show.called


def test_hide_busy():
    """Test busy indicator hide."""
    with patch('guizero.App'):
        with patch('guizero.PushButton'):
            with patch('guizero.Text'):
                with patch('guizero.Picture'):
                    with patch('guizero.Window') as mock_window:
                        with patch('RPi.GPIO'):
                            import pidslm
                            app = pidslm.piDSLM()
                            
                            # Mock the busy window
                            mock_busy_window = MagicMock()
                            app.busy = mock_busy_window
                            
                            with patch('builtins.print'):
                                app.hide_busy()
                                
                                # Verify busy window was hidden
                                assert mock_busy_window.hide.called

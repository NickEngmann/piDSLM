"""Tests for pidslm.py initialization and basic functionality."""

import pytest
import sys
import os
from unittest.mock import patch, MagicMock, call

# Add the repo directory to the path
sys.path.insert(0, '')


def test_app_initialization():
    """Test that the piDSLM app initializes correctly."""
    with patch('guizero.App') as mock_app:
        with patch('guizero.PushButton'):
            with patch('guizero.Text'):
                with patch('guizero.Picture'):
                    with patch('guizero.Window'):
                        with patch('RPi.GPIO') as mock_gpio:
                            # Clear any cached imports
                            if 'pidslm' in sys.modules:
                                del sys.modules['pidslm']
                            import pidslm
                            app = pidslm.piDSLM()
                            assert app is not None
                            # App should have created the main window
                            assert hasattr(app, 'app')
                            # Verify GPIO was set up
                            assert mock_gpio.setmode.called
                            assert mock_gpio.setup.called


def test_timestamp():
    """Test timestamp generation."""
    import pidslm
    
    app = pidslm.piDSLM()
    timestamp = app.timestamp()
    
    # Timestamp should be in format YYYYMMDD_HHMMSS
    assert len(timestamp) == 15  # 8 for date + 1 for underscore + 6 for time
    assert '_' in timestamp


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

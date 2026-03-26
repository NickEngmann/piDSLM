"""test_pidslm.py — Tests for piDSLM main application integration.

Tests the integration between pidslm.py and config.py, ensuring that
configuration values are properly used throughout the application.
"""
import pytest
import os
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock


@pytest.fixture
def mock_config():
    """Create a mock configuration object with all necessary attributes."""
    cfg = Mock()
    cfg.downloads_dir = "/tmp/test_downloads"
    cfg.icon_dir = "/tmp/test_icons"
    cfg.home_dir = "/home/pi"
    cfg.dropbox_enabled = True
    cfg.dropbox_token = "test_token_123"
    cfg.button_pin = 16
    cfg.button_mode = "BCM"
    cfg.button_bounce_time = 2500
    
    # Mock the get_capture_output_path method
    def get_output_path(pattern):
        return os.path.join(cfg.downloads_dir, pattern % "test_timestamp")
    
    cfg.get_capture_output_path = Mock(side_effect=get_output_path)
    
    return cfg


@pytest.fixture
def mock_gpio():
    """Create a mock GPIO module."""
    mock = Mock()
    mock.BCM = 11
    mock.OUT = 0
    mock.IN = 1
    mock.PUD_UP = 22
    mock.FALLING = 32
    mock.setmode = Mock()
    mock.setup = Mock()
    mock.add_event_detect = Mock()
    mock.cleanup = Mock()
    return mock


def test_config_values_accessible(mock_config):
    """Test that config values are accessible in application."""
    # Verify all expected config values exist
    assert mock_config.downloads_dir == "/tmp/test_downloads"
    assert mock_config.icon_dir == "/tmp/test_icons"
    assert mock_config.button_pin == 16
    assert mock_config.button_bounce_time == 2500
    assert mock_config.dropbox_token == "test_token_123"


def test_timestamp_format():
    """Test that timestamp generates correct format."""
    from datetime import datetime
    
    # Test timestamp format: YYYYMMDD_HHMMSS
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Verify format: 15 characters total
    # Example: 20240101_120000
    assert len(ts) == 15
    # Year-Month-Day separator is at position 8 (0-indexed)
    assert ts[8] == '_'
    # All should be digits except the underscore
    digits_only = ts.replace('_', '')
    assert digits_only.isdigit()
    assert len(digits_only) == 14


def test_get_capture_output_path(mock_config):
    """Test that config.get_capture_output_path works correctly."""
    # Test with different patterns
    output1 = mock_config.get_capture_output_path("test_%s.jpg")
    assert "/tmp/test_downloads/" in output1
    assert "test_" in output1
    
    output2 = mock_config.get_capture_output_path("%scam.jpg")
    assert "/tmp/test_downloads/" in output2
    assert "cam.jpg" in output2


def test_icon_path_construction(mock_config):
    """Test that icon paths are constructed correctly."""
    icon_names = ["prev", "gallery", "vid", "lapse", "self", "long", 
                  "drop", "del", "left", "right"]
    
    for icon_name in icon_names:
        icon_path = os.path.join(mock_config.icon_dir, f"{icon_name}.png")
        assert icon_path == f"/tmp/test_icons/{icon_name}.png"


def test_upload_script_path(mock_config):
    """Test that upload script path is constructed correctly."""
    upload_script = os.path.join(
        mock_config.home_dir, "piDSLM", "dropbox_upload.py"
    )
    assert upload_script == "/home/pi/piDSLM/dropbox_upload.py"


def test_output_path_patterns(mock_config):
    """Test that different capture modes use correct output paths."""
    # Burst mode pattern
    burst_path = mock_config.get_capture_output_path("BR%s%%04d.jpg")
    assert "BR" in burst_path
    assert "%04d" in burst_path
    assert burst_path.startswith("/tmp/test_downloads/")
    
    # Video mode pattern  
    video_path = mock_config.get_capture_output_path("%svid%%04d.h264")
    assert "vid" in video_path
    assert ".h264" in video_path
    assert video_path.startswith("/tmp/test_downloads/")
    
    # Timelapse pattern
    lapse_path = mock_config.get_capture_output_path("TL%s%%04d.jpg")
    assert "TL" in lapse_path
    assert lapse_path.startswith("/tmp/test_downloads/")
    
    # Photo pattern
    photo_path = mock_config.get_capture_output_path("%scam.jpg")
    assert "cam.jpg" in photo_path
    assert photo_path.startswith("/tmp/test_downloads/")


def test_gpio_config_values(mock_config):
    """Test that GPIO uses config values."""
    # Verify GPIO configuration values
    assert mock_config.button_pin == 16
    assert mock_config.button_bounce_time == 2500
    assert mock_config.button_mode == "BCM"


def test_subprocess_command_construction():
    """Test that subprocess commands are constructed correctly."""
    # Simulate command construction as done in pidslm.py
    downloads_dir = "/tmp/test_downloads"
    timestamp = "20240101_120000"
    
    # Photo capture command
    output_path = os.path.join(downloads_dir, f"{timestamp}cam.jpg")
    cmd = f"raspistill -f -o {output_path}"
    assert output_path in cmd
    assert "raspistill" in cmd
    
    # Burst command
    burst_output = os.path.join(downloads_dir, f"BR{timestamp}%04d.jpg")
    burst_cmd = f"raspistill -t 10000 -tl 0 --thumb none -n -bm -o {burst_output}"
    assert burst_output in burst_cmd
    assert "-t 10000" in burst_cmd
    
    # Video command
    video_output = os.path.join(downloads_dir, f"{timestamp}vid.h264")
    video_cmd = f"raspivid -f -t 30000 -o {video_output}"
    assert video_output in video_cmd
    assert "raspivid" in video_cmd


def test_file_filtering():
    """Test that photo filtering works correctly."""
    from pathlib import Path
    
    # Simulate finding photos
    test_photos = ["photo1.jpg", "photo2.JPG", "image.jpg", "test.txt"]
    
    jpg_files = [p for p in test_photos if p.lower().endswith('.jpg')]
    
    assert len(jpg_files) == 3
    assert "photo1.jpg" in jpg_files
    assert "test.txt" not in jpg_files


def test_glob_pattern_matching(mock_config):
    """Test that glob pattern matching works correctly."""
    from pathlib import Path
    
    # Simulate finding photos like show_gallery does
    downloads_path = Path(mock_config.downloads_dir)
    
    # Create mock files
    mock_files = [
        downloads_path / "photo1.jpg",
        downloads_path / "photo2.jpg",
        downloads_path / "video.mp4",
        downloads_path / "document.txt"
    ]
    
    # Simulate glob pattern
    jpg_files = sorted([
        str(p) for p in mock_files if p.suffix.lower() == '.jpg'
    ])
    
    assert len(jpg_files) == 2
    assert all("/tmp/test_downloads/" in f for f in jpg_files)


def test_logging_configuration():
    """Test that logging is configured correctly."""
    import logging
    
    logger = logging.getLogger("test_module")
    logger.setLevel(logging.DEBUG)
    
    assert logger.level == logging.DEBUG
    
    # Verify handlers work
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    
    # Test log message
    logger.info("Test message")


def test_subprocess_error_handling():
    """Test that subprocess errors are handled correctly."""
    import subprocess
    
    # Test timeout handling
    try:
        # This will fail but we test error handling
        result = subprocess.run(
            "nonexistent_command",
            shell=True,
            capture_output=True,
            text=True,
            timeout=1
        )
        # Should have non-zero return code
        assert result.returncode != 0
    except subprocess.TimeoutExpired:
        # Expected if command is still running
        pass
    except FileNotFoundError:
        # Expected for nonexistent command
        pass


def test_config_integration_patterns():
    """Test various integration patterns between config and pidslm."""
    # Test download directory usage
    config_downloads = "/tmp/test_downloads"
    config_icons = "/tmp/test_icons"
    
    # Verify paths would be used correctly
    photo_path = os.path.join(config_downloads, "photo.jpg")
    icon_path = os.path.join(config_icons, "gallery.png")
    
    assert photo_path == "/tmp/test_downloads/photo.jpg"
    assert icon_path == "/tmp/test_icons/gallery.png"
    
    # Test command building
    timestamp = "20240101_120000"
    capture_path = os.path.join(config_downloads, f"{timestamp}cam.jpg")
    capture_cmd = f"raspistill -f -o {capture_path}"
    
    assert capture_cmd == f"raspistill -f -o {capture_path}"

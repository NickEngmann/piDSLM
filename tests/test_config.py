"""test_config.py — Tests for configuration module."""
import pytest
import os
from unittest.mock import patch

# Import config module
from config import PiDSLMConfig, get_config, set_config, config


@pytest.fixture
def reset_config():
    """Reset global config before and after test."""
    from config import config as global_config
    # Store original
    original = global_config
    # Reset
    from config import config
    # Import internal module state
    import sys
    sys.modules['config']._config_state = None
    yield
    # Restore
    import sys
    if 'config' in sys.modules:
        config_module = sys.modules['config']
        if hasattr(config_module, '_config_state'):
            config_module._config_state = original


def test_default_config():
    """Test default configuration values."""
    cfg = PiDSLMConfig()
    
    assert cfg.downloads_dir == os.path.expanduser("~/Downloads")
    assert cfg.dropbox_enabled is False
    assert cfg.dropbox_token is None
    assert cfg.button_pin == 16
    assert cfg.button_mode == "BCM"


def test_config_from_env():
    """Test configuration from environment variables."""
    with patch.dict(os.environ, {
        "PIDSLM_DOWNLOADS_DIR": "/custom/path/Downloads",
        "PIDSLM_ICON_DIR": "/custom/icons",
        "DROPBOX_ACCESS_TOKEN": "test_token_123"
    }):
        cfg = PiDSLMConfig.from_env()
        
        assert cfg.downloads_dir == "/custom/path/Downloads"
        assert cfg.icon_dir == "/custom/icons"
        assert cfg.dropbox_enabled is True
        assert cfg.dropbox_token == "test_token_123"


def test_get_icon_path():
    """Test icon path resolution."""
    cfg = PiDSLMConfig()
    cfg.icon_dir = "/test/icons"
    
    icon_path = cfg.get_icon_path("cam")
    assert icon_path == "/test/icons/cam.png"
    
    icon_path = cfg.get_icon_path("gallery")
    assert icon_path == "/test/icons/gallery.png"


def test_get_capture_output_path():
    """Test capture output path resolution."""
    cfg = PiDSLMConfig()
    cfg.downloads_dir = "/test/downloads"
    
    output_path = cfg.get_capture_output_path("20240101_120000cam.jpg")
    assert output_path == "/test/downloads/20240101_120000cam.jpg"


def test_get_config_default():
    """Test get_config returns default when none set."""
    # Clear global config
    from config import config as global_config
    import sys
    
    # Create fresh module reference
    sys.modules['config']._config_state = None
    
    cfg = get_config()
    assert isinstance(cfg, PiDSLMConfig)


def test_set_config():
    """Test setting global configuration."""
    custom_config = PiDSLMConfig()
    custom_config.downloads_dir = "/custom/test"
    
    set_config(custom_config)
    
    cfg = get_config()
    assert cfg.downloads_dir == "/custom/test"


def test_environment_variables_not_set():
    """Test config when environment variables are not set."""
    # Ensure no PIDSLM vars are set
    with patch.dict(os.environ, {}, clear=False):
        # Remove if exists
        for var in ["PIDSLM_DOWNLOADS_DIR", "PIDSLM_ICON_DIR", "DROPBOX_ACCESS_TOKEN"]:
            os.environ.pop(var, None)
        
        cfg = PiDSLMConfig.from_env()
        
        assert cfg.downloads_dir == os.path.expanduser("~/Downloads")
        assert cfg.dropbox_enabled is False


def test_capture_settings_defaults():
    """Test default capture timing settings."""
    cfg = PiDSLMConfig()
    
    assert cfg.burst_duration_ms == 10000
    assert cfg.lapse_duration_ms == 3600000  # 1 hour
    assert cfg.lapse_interval_ms == 60000  # 1 minute intervals
    assert cfg.video_capture_duration_ms == 30000  # 30 seconds
    assert cfg.split_video_total_duration_ms == 1800000  # 30 minutes
    assert cfg.split_video_segment_ms == 300000  # 5 minute segments

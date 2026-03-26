"""Configuration module for piDSLM.

Provides centralized configuration management for:
- File paths (Downloads, icons, etc.)
- Dropbox settings
- GPIO settings
"""
import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class PiDSLMConfig:
    """Configuration for the Pi DSLM camera interface."""
    
    # Paths
    downloads_dir: str = os.path.expanduser("~/Downloads")
    icon_dir: str = os.path.join(os.path.dirname(__file__), "icon")
    home_dir: str = os.path.expanduser("~/pi")
    
    # Dropbox settings
    dropbox_folder_name: str = "Downloads"
    dropbox_enabled: bool = False
    dropbox_token: Optional[str] = None
    
    # GPIO settings
    button_pin: int = 16
    button_mode: str = "BCM"
    button_bounce_time: int = 2500
    
    # Capture settings
    burst_duration_ms: int = 10000
    lapse_duration_ms: int = 3600000
    lapse_interval_ms: int = 60000
    video_capture_duration_ms: int = 30000
    split_video_total_duration_ms: int = 1800000
    split_video_segment_ms: int = 300000
    
    @classmethod
    def from_env(cls) -> "PiDSLMConfig":
        """Create configuration from environment variables."""
        config = cls()
        
        downloads_path = os.environ.get("PIDSLM_DOWNLOADS_DIR")
        if downloads_path:
            config.downloads_dir = os.path.expanduser(downloads_path)
        
        icon_path = os.environ.get("PIDSLM_ICON_DIR")
        if icon_path:
            config.icon_dir = icon_path
        
        dropbox_token = os.environ.get("DROPBOX_ACCESS_TOKEN")
        if dropbox_token:
            config.dropbox_enabled = True
            config.dropbox_token = dropbox_token
        
        return config
    
    def get_icon_path(self, icon_name: str) -> str:
        """Get full path to an icon file."""
        return os.path.join(self.icon_dir, f"{icon_name}.png")
    
    def get_capture_output_path(self, filename: str) -> str:
        """Get full path to capture output in downloads directory."""
        return os.path.join(self.downloads_dir, filename)


# Global configuration instance (will be set by main app)
config: Optional[PiDSLMConfig] = None


def get_config() -> PiDSLMConfig:
    """Get the global configuration, creating default if needed."""
    global config
    if config is None:
        config = PiDSLMConfig.from_env()
    return config


def set_config(cfg: PiDSLMConfig):
    """Set the global configuration."""
    global config
    config = cfg

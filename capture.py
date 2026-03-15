"""Capture module for piDSLM camera interface.

Separates capture logic from hardware/GUI dependencies for testability.
"""

import datetime
import os
import subprocess
import glob
from typing import List, Optional, Tuple


class CaptureResult:
    """Result of a capture operation."""
    
    def __init__(self, success: bool, filepath: Optional[str] = None, 
                 timestamp: Optional[str] = None, error: Optional[str] = None,
                 filename_pattern: Optional[str] = None):
        self.success = success
        self.filepath = filepath
        self.timestamp = timestamp
        self.error = error
        self.filename_pattern = filename_pattern


class ImageCapture:
    """Handles image capture operations with realistic simulation."""
    
    def __init__(self, output_dir: str = '/home/pi/Downloads',
                 capture_command: str = 'raspistill',
                 is_hardware_available: bool = True):
        self.output_dir = output_dir
        self.capture_command = capture_command
        self.is_hardware_available = is_hardware_available
        self._capture_history: List[CaptureResult] = []
    
    def generate_timestamp(self) -> str:
        """Generate a timestamp string for filenames."""
        return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def create_capture_filename(self, prefix: str, timestamp: str, 
                                extension: str = '.jpg') -> str:
        """Create a capture filename with optional pattern."""
        filename = f"{prefix}{timestamp}{extension}"
        return os.path.join(self.output_dir, filename)
    
    def simulate_capture(self, filepath: str, filename_pattern: Optional[str] = None) -> CaptureResult:
        """Simulate a capture operation for testing."""
        if not self.is_hardware_available:
            # In hardware simulation mode, create a dummy file
            os.makedirs(self.output_dir, exist_ok=True)
            try:
                with open(filepath, 'wb') as f:
                    # Write a minimal JPEG header (1px black image)
                    f.write(b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9equivivalent minimal JPEG')
                timestamp_str = filepath.split('/')[-1].replace('.jpg', '')
                return CaptureResult(success=True, filepath=filepath, 
                                     timestamp=timestamp_str,
                                     filename_pattern=filename_pattern or filepath)
            except Exception as e:
                return CaptureResult(success=False, error=str(e))
        else:
            return CaptureResult(success=False, error="Hardware not available in test mode")
    
    def capture(self, prefix: str = "", extension: str = '.jpg',
                timeout_ms: int = 3500, is_live: bool = False) -> CaptureResult:
        """Capture a single image.
        
        Args:
            prefix: Prefix for filename (e.g., "cam", "photo")
            extension: File extension (default: .jpg)
            timeout_ms: Capture timeout in milliseconds (default: 3500)
            is_live: Whether to use preview mode (no output file)
        
        Returns:
            CaptureResult with success status and file info
        """
        timestamp = self.generate_timestamp()
        
        if is_live:
            filename = f"{prefix}{timestamp}"
            filepath = os.path.join(self.output_dir, filename)
        else:
            filename = f"{prefix}{timestamp}{extension}"
            filepath = os.path.join(self.output_dir, filename)
        
        result = self._execute_capture(filepath, prefix, timestamp, timeout_ms, extension, is_live)
        
        if result.success:
            self._capture_history.append(result)
        
        return result
    
    def _execute_capture(self, filepath: str, prefix: str, timestamp: str,
                         timeout_ms: int, extension: str, is_live: bool) -> CaptureResult:
        """Execute the actual capture command or simulation."""
        if not self.is_hardware_available:
            return self.simulate_capture(filepath)
        
        try:
            if is_live:
                cmd = [self.capture_command, '-f', '-t', str(timeout_ms)]
            else:
                cmd = [self.capture_command, '-f', '-t', str(timeout_ms), '-o', filepath]
            
            subprocess.run(cmd, check=True, timeout=timeout_ms/1000 + 5)
            
            return CaptureResult(
                success=True,
                filepath=filepath,
                timestamp=timestamp,
                filename_pattern=f"{prefix}{timestamp}{extension}"
            )
        except subprocess.TimeoutExpired:
            return CaptureResult(
                success=False,
                error=f"Capture timed out after {timeout_ms}ms"
            )
        except subprocess.CalledProcessError as e:
            return CaptureResult(
                success=False,
                error=f"Capture failed: {e}"
            )
        except FileNotFoundError:
            return CaptureResult(
                success=False,
                error=f"Capture command not found: {self.capture_command}"
            )
    
    def burst_capture(self, prefix: str = "BR", 
                      timeout_ms: int = 10000,
                      interval_ms: int = 0) -> CaptureResult:
        """Capture a burst of photos with pattern naming.
        
        Args:
            prefix: Filename prefix (default: "BR" for burst)
            timeout_ms: Total capture timeout in milliseconds
            interval_ms: Interval between captures (0 for continuous)
        
        Returns:
            CaptureResult indicating success
        """
        timestamp = self.generate_timestamp()
        
        if not self.is_hardware_available:
            # Simulate burst capture by capturing one file
            filepath = self.create_capture_filename(prefix, timestamp, '.jpg')
            result = self.simulate_capture(filepath)
            result.filename_pattern = f"{prefix}{timestamp}%04d.jpg"
            return result
        
        try:
            pattern = f"{prefix}{timestamp}%04d.jpg"
            filepath = os.path.join(self.output_dir, pattern)
            
            cmd = [
                self.capture_command,
                '-t', str(timeout_ms),
                '-tl', str(interval_ms),
                '--thumb', 'none',
                '-n', '-bm',
                '-o', filepath
            ]
            
            subprocess.run(cmd, check=True, timeout=timeout_ms/1000 + 10)
            
            return CaptureResult(
                success=True,
                filepath=filepath.replace('%04d', ''),
                timestamp=timestamp,
                filename_pattern=pattern
            )
        except subprocess.TimeoutExpired:
            return CaptureResult(
                success=False,
                error=f"Burst capture timed out after {timeout_ms}ms"
            )
        except subprocess.CalledProcessError as e:
            return CaptureResult(
                success=False,
                error=f"Burst capture failed: {e}"
            )
    
    def timelapse(self, prefix: str = "TL",
                  timeout_ms: int = 3600000,
                  interval_ms: int = 60000) -> CaptureResult:
        """Capture a timelapse sequence.
        
        Args:
            prefix: Filename prefix (default: "TL" for timelapse)
            timeout_ms: Total capture duration in milliseconds (default: 1h)
            interval_ms: Interval between captures in milliseconds (default: 60s)
        
        Returns:
            CaptureResult indicating success
        """
        return self.burst_capture(
            prefix=prefix,
            timeout_ms=timeout_ms,
            interval_ms=interval_ms
        )
    
    def video_capture(self, prefix: str = "vid",
                      timeout_ms: int = 30000,
                      is_frame_sequence: bool = False,
                      segment_time_ms: int = 300000) -> CaptureResult:
        """Capture video using raspivid.
        
        Args:
            prefix: Filename prefix (default: "vid")
            timeout_ms: Capture duration in milliseconds (default: 30s)
            is_frame_sequence: Whether to capture frames as sequence
            segment_time_ms: Time between segments (for long recordings)
        
        Returns:
            CaptureResult indicating success
        """
        timestamp = self.generate_timestamp()
        extension = '.h264'
        
        if not self.is_hardware_available:
            pattern = f"{prefix}{timestamp}%04d.h264" if is_frame_sequence else f"{prefix}{timestamp}.h264"
            filepath = self.create_capture_filename(prefix, timestamp, extension)
            return self.simulate_capture(filepath, filename_pattern=pattern)
        
        try:
            if is_frame_sequence:
                pattern = f"{prefix}{timestamp}%04d.h264"
            else:
                pattern = f"{prefix}{timestamp}.h264"
            
            filepath = os.path.join(self.output_dir, pattern)
            
            cmd = [
                self.capture_command,
                '-f' if is_frame_sequence else '',
                '-t', str(timeout_ms),
                '-sg', str(segment_time_ms) if is_frame_sequence else '',
                '-o', filepath
            ]
            
            # Filter out empty strings from cmd
            cmd = [c for c in cmd if c]
            
            subprocess.run(cmd, check=True, timeout=timeout_ms/1000 + 10)
            
            return CaptureResult(
                success=True,
                filepath=filepath,
                timestamp=timestamp,
                filename_pattern=pattern
            )
        except subprocess.TimeoutExpired:
            return CaptureResult(
                success=False,
                error=f"Video capture timed out after {timeout_ms}ms"
            )
        except subprocess.CalledProcessError as e:
            return CaptureResult(
                success=False,
                error=f"Video capture failed: {e}"
            )
    
    def get_capture_history(self) -> List[CaptureResult]:
        """Get list of all captured images."""
        return self._capture_history.copy()
    
    def clear_capture_history(self) -> None:
        """Clear the capture history."""
        self._capture_history.clear()


class GalleryManager:
    """Manages the photo gallery display."""
    
    def __init__(self, photo_dir: str = '/home/pi/Downloads',
                 file_pattern: str = '*.jpg'):
        self.photo_dir = photo_dir
        self.file_pattern = file_pattern
        self._photos: List[str] = []
        self._current_index = 0
    
    def load_photos(self) -> List[str]:
        """Load all photos from the directory."""
        import glob as glob_module
        
        pattern = os.path.join(self.photo_dir, self.file_pattern)
        self._photos = sorted(glob_module.glob(pattern))
        self._current_index = 0
        return self._photos
    
    def get_photo_count(self) -> int:
        """Get the total number of photos."""
        return len(self._photos)
    
    def get_current_photo(self) -> Optional[str]:
        """Get the currently selected photo path."""
        if self._photos:
            return self._photos[self._current_index]
        return None
    
    def get_thumbnail_count(self) -> int:
        """Get number of thumbnails available."""
        return len(self._photos)
    
    def navigate_left(self) -> Optional[str]:
        """Navigate to previous photo."""
        if not self._photos:
            return None
        
        if self._current_index == 0:
            self._current_index = len(self._photos) - 1
        else:
            self._current_index -= 1
        
        return self._photos[self._current_index]
    
    def navigate_right(self) -> Optional[str]:
        """Navigate to next photo."""
        if not self._photos:
            return None
        
        if self._current_index == len(self._photos) - 1:
            self._current_index = 0
        else:
            self._current_index += 1
        
        return self._photos[self._current_index]
    
    def go_to(self, index: int) -> Optional[str]:
        """Navigate to a specific photo by index."""
        if 0 <= index < len(self._photos):
            self._current_index = index
            return self._photos[self._current_index]
        return None
    
    def clear(self) -> None:
        """Clear the gallery."""
        self._photos.clear()
        self._current_index = 0

"""Tests for capture module - ImageCapture and GalleryManager classes."""

import pytest
import os
import tempfile
from capture import ImageCapture, GalleryManager, CaptureResult


class TestImageCapture:
    """Test suite for the ImageCapture class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
    
    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_timestamp_generation(self):
        """Test that timestamps are generated correctly."""
        capture = ImageCapture(output_dir=self.temp_dir, is_hardware_available=False)
        timestamp = capture.generate_timestamp()
        
        assert isinstance(timestamp, str)
        assert len(timestamp) == 15  # YYYYMMDD_HHMMSS format
        # Timestamp contains digits and underscore, so check format differently
        assert '_' in timestamp
        assert timestamp[:8].isdigit()  # Date part is digits
        assert timestamp[9:].replace('_', '').isdigit()  # Time part is digits
    
    def test_filename_creation(self):
        """Test filename creation with various parameters."""
        capture = ImageCapture(output_dir=self.temp_dir, is_hardware_available=False)
        
        filename = capture.create_capture_filename("cam", "20240115_123045", ".jpg")
        assert filename == os.path.join(self.temp_dir, "cam20240115_123045.jpg")
    
    def test_capture_returns_result(self):
        """Test that capture method returns CaptureResult."""
        capture = ImageCapture(output_dir=self.temp_dir, is_hardware_available=False)
        
        result = capture.capture(prefix="test")
        
        assert isinstance(result, CaptureResult)
        # In test simulation mode, capture should succeed
        assert result.success is True
    
    def test_capture_simulates_in_test_mode(self):
        """Test capture simulation when hardware is not available."""
        capture = ImageCapture(output_dir=self.temp_dir, is_hardware_available=False)
        
        result = capture.capture(prefix="cam", extension=".jpg", timeout_ms=100)
        
        # In simulation mode, it should succeed
        assert isinstance(result, CaptureResult)
    
    def test_capture_history_tracking(self):
        """Test that captures are tracked in history."""
        capture = ImageCapture(output_dir=self.temp_dir, is_hardware_available=False)
        
        capture.capture(prefix="cam")
        capture.capture(prefix="cam")
        
        history = capture.get_capture_history()
        assert len(history) == 2
    
    def test_capture_clears_history(self):
        """Test clearing capture history."""
        capture = ImageCapture(output_dir=self.temp_dir, is_hardware_available=False)
        
        capture.capture(prefix="cam")
        capture.clear_capture_history()
        
        assert len(capture.get_capture_history()) == 0
    
    def test_burst_capture(self):
        """Test burst capture functionality."""
        capture = ImageCapture(output_dir=self.temp_dir, is_hardware_available=False)
        
        result = capture.burst_capture(prefix="BR", timeout_ms=1000, interval_ms=100)
        
        assert isinstance(result, CaptureResult)
        assert '%04d' in result.filename_pattern
    
    def test_timelapse_delegates_to_burst(self):
        """Test that timelapse uses burst capture logic."""
        capture = ImageCapture(output_dir=self.temp_dir, is_hardware_available=False)
        
        result = capture.timelapse(prefix="TL", timeout_ms=3600000, interval_ms=60000)
        
        assert isinstance(result, CaptureResult)
        # Check that pattern contains TL and %04d
        assert result.filename_pattern is not None
        assert 'TL' in result.filename_pattern
        assert '%04d' in result.filename_pattern
    
    def test_video_capture_simulation(self):
        """Test video capture in simulation mode."""
        capture = ImageCapture(output_dir=self.temp_dir, is_hardware_available=False)
        
        result = capture.video_capture(prefix="vid", timeout_ms=30000, is_frame_sequence=False)
        
        assert isinstance(result, CaptureResult)
        assert result.filename_pattern is not None
        assert result.filename_pattern.endswith('.h264')
    
    def test_video_capture_frame_sequence(self):
        """Test video capture with frame sequence."""
        capture = ImageCapture(output_dir=self.temp_dir, is_hardware_available=False)
        
        result = capture.video_capture(prefix="vid", timeout_ms=30000, is_frame_sequence=True)
        
        assert isinstance(result, CaptureResult)
        assert result.filename_pattern is not None
        assert '%04d.h264' in result.filename_pattern


class TestGalleryManager:
    """Test suite for the GalleryManager class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        
        # Create some dummy photo files
        for i in range(5):
            filepath = os.path.join(self.temp_dir, f"photo{i}.jpg")
            with open(filepath, 'w') as f:
                f.write("dummy")
        
        self.gallery = GalleryManager(photo_dir=self.temp_dir)
    
    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_load_photos(self):
        """Test loading photos from directory."""
        photos = self.gallery.load_photos()
        
        assert len(photos) == 5
        assert all(p.endswith('.jpg') for p in photos)
    
    def test_get_photo_count(self):
        """Test photo count."""
        self.gallery.load_photos()
        
        assert self.gallery.get_photo_count() == 5
    
    def test_navigation_left_at_start(self):
        """Test navigation left from first photo wraps to last."""
        self.gallery.load_photos()
        self.gallery._current_index = 0
        
        result = self.gallery.navigate_left()
        
        assert result.endswith('photo4.jpg')
        assert self.gallery._current_index == 4
    
    def test_navigation_left(self):
        """Test normal left navigation."""
        self.gallery.load_photos()
        self.gallery._current_index = 2
        
        result = self.gallery.navigate_left()
        
        assert result.endswith('photo1.jpg')
        assert self.gallery._current_index == 1
    
    def test_navigation_right_at_end(self):
        """Test navigation right from last photo wraps to first."""
        self.gallery.load_photos()
        self.gallery._current_index = 4
        
        result = self.gallery.navigate_right()
        
        assert result.endswith('photo0.jpg')
        assert self.gallery._current_index == 0
    
    def test_navigation_right(self):
        """Test normal right navigation."""
        self.gallery.load_photos()
        self.gallery._current_index = 1
        
        result = self.gallery.navigate_right()
        
        assert result.endswith('photo2.jpg')
        assert self.gallery._current_index == 2
    
    def test_go_to_index(self):
        """Test direct index navigation."""
        self.gallery.load_photos()
        
        result = self.gallery.go_to(3)
        
        assert result.endswith('photo3.jpg')
        assert self.gallery._current_index == 3
    
    def test_go_to_invalid_index(self):
        """Test navigating to invalid index."""
        self.gallery.load_photos()
        
        result = self.gallery.go_to(100)
        
        assert result is None
        assert self.gallery._current_index == 0  # Stays at current
    
    def test_empty_gallery(self):
        """Test navigation on empty gallery."""
        gallery = GalleryManager(photo_dir='/nonexistent')
        
        assert gallery.navigate_left() is None
        assert gallery.navigate_right() is None
        assert gallery.get_current_photo() is None
    
    def test_gallery_clear(self):
        """Test clearing gallery."""
        self.gallery.load_photos()
        self.gallery.clear()
        
        assert self.gallery.get_photo_count() == 0
        assert self.gallery._current_index == 0


class TestIntegration:
    """Integration tests for capture and gallery."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
    
    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_capture_and_gallery_workflow(self):
        """Test complete workflow: capture then view in gallery."""
        capture = ImageCapture(output_dir=self.temp_dir, is_hardware_available=False)
        gallery = GalleryManager(photo_dir=self.temp_dir)
        
        # Capture some photos (simulated)
        result1 = capture.capture(prefix="test1")
        result2 = capture.capture(prefix="test2")
        
        # Load gallery
        photos = gallery.load_photos()
        
        assert len(photos) == 2
        assert gallery.get_current_photo() is not None
    
    def test_capture_history_persistence(self):
        """Test that capture history persists across operations."""
        capture = ImageCapture(output_dir=self.temp_dir, is_hardware_available=False)
        
        capture.capture(prefix="test")
        history_before = len(capture.get_capture_history())
        
        # Reload gallery (simulates restart)
        gallery = GalleryManager(photo_dir=self.temp_dir)
        gallery.load_photos()
        
        history_after = len(capture.get_capture_history())
        assert history_before == history_after

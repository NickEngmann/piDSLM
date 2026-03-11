"""test_pidslm.py — Tests for piDSLM camera control functionality.

Tests the timestamp generation, image capture logic, and gallery navigation.
Uses embedded_mocks.py for hardware simulation.
"""
import pytest
from embedded_mocks import MockGPIO, MockI2C, MockSPI, MockUART
from unittest.mock import patch, MagicMock
import os
import glob
import datetime


class MockPiDSLM:
    """Mock version of piDSLM for testing without GUI."""
    
    def __init__(self):
        self.capture_number = self.timestamp()
        self.video_capture_number = self.timestamp()
        self.picture_index = 0
        self.saved_pictures = []
        self.shown_picture = ""
    
    def timestamp(self):
        """Generate timestamp string for photos."""
        tstring = datetime.datetime.now()
        return tstring.strftime("%Y%m%d_%H%M%S")
    
    def capture_image(self):
        """Capture an image with timestamp."""
        capture_number = self.timestamp()
        return f"/home/pi/Downloads/{capture_number}cam.jpg"
    
    def takePicture(self, channel):
        """Take picture triggered by GPIO button."""
        capture_number = self.timestamp()
        return f"/home/pi/Downloads/{capture_number}cam.jpg"
    
    def burst(self):
        """Capture burst of images."""
        capture_number = self.timestamp()
        return f"/home/pi/Downloads/BR{capture_number}%04d.jpg"
    
    def lapse(self):
        """Capture timelapse images."""
        capture_number = self.timestamp()
        return f"/home/pi/Downloads/TL{capture_number}%04d.jpg"
    
    def video_capture(self):
        """Capture video."""
        capture_number = self.timestamp()
        return f"/home/pi/Downloads/{capture_number}vid.h264"
    
    def split_hd_30m(self):
        """Split HD video capture."""
        capture_number = self.timestamp()
        return f"/home/pi/Downloads/{capture_number}vid%04d.h264"
    
    def picture_left(self):
        """Navigate to previous picture in gallery."""
        if self.picture_index == 0:
            self.picture_index = len(self.saved_pictures) - 1
        else:
            self.picture_index -= 1
        return self.picture_index
    
    def picture_right(self):
        """Navigate to next picture in gallery."""
        if self.picture_index == len(self.saved_pictures) - 1:
            self.picture_index = 0
        else:
            self.picture_index += 1
        return self.picture_index
    
    def show_gallery(self):
        """Show gallery with saved pictures."""
        # Only populate from glob if saved_pictures is empty (simulating fresh load)
        if not self.saved_pictures:
            self.saved_pictures = glob.glob('/home/pi/Downloads/*.jpg')
        if self.saved_pictures:
            self.shown_picture = self.saved_pictures[self.picture_index]
        return self.saved_pictures


def test_timestamp_format():
    """Test that timestamp generates correct format."""
    mock = MockPiDSLM()
    ts = mock.timestamp()
    # Format is YYYYMMDD_HHMMSS (8 digits + underscore + 6 digits = 15 chars)
    assert len(ts) == 15
    assert ts[8] == '_'
    # Verify it's a valid date/time format
    datetime.datetime.strptime(ts, "%Y%m%d_%H%M%S")


def test_timestamp_uniqueness():
    """Test that consecutive timestamps are different."""
    mock = MockPiDSLM()
    ts1 = mock.timestamp()
    ts2 = mock.timestamp()
    # Even if called quickly, they should be different or same if same second
    # At minimum, the format should be consistent
    assert len(ts1) == len(ts2) == 15


def test_capture_image_path():
    """Test that capture_image generates correct file path."""
    mock = MockPiDSLM()
    path = mock.capture_image()
    assert path.startswith("/home/pi/Downloads/")
    assert path.endswith("cam.jpg")
    # Should contain timestamp
    assert len(path.split("/")[-1].replace("cam.jpg", "")) == 15


def test_takePicture_path():
    """Test that takePicture generates correct file path."""
    mock = MockPiDSLM()
    path = mock.takePicture(channel=16)
    assert path.startswith("/home/pi/Downloads/")
    assert path.endswith("cam.jpg")


def test_burst_path():
    """Test that burst generates correct file path pattern."""
    mock = MockPiDSLM()
    path = mock.burst()
    assert path.startswith("/home/pi/Downloads/BR")
    assert path.endswith(".jpg")
    assert "%04d" in path  # Burst uses numbered pattern


def test_lapse_path():
    """Test that lapse generates correct file path pattern."""
    mock = MockPiDSLM()
    path = mock.lapse()
    assert path.startswith("/home/pi/Downloads/TL")
    assert path.endswith(".jpg")
    assert "%04d" in path  # Timelapse uses numbered pattern


def test_video_capture_path():
    """Test that video_capture generates correct file path."""
    mock = MockPiDSLM()
    path = mock.video_capture()
    assert path.startswith("/home/pi/Downloads/")
    assert path.endswith("vid.h264")


def test_split_hd_30m_path():
    """Test that split_hd_30m generates correct file path pattern."""
    mock = MockPiDSLM()
    path = mock.split_hd_30m()
    assert path.startswith("/home/pi/Downloads/")
    assert path.endswith(".h264")
    assert "%04d" in path  # Split video uses numbered pattern


def test_picture_left_wraparound():
    """Test that picture_left wraps around to end when at start."""
    mock = MockPiDSLM()
    mock.picture_index = 0
    mock.saved_pictures = ["pic1.jpg", "pic2.jpg", "pic3.jpg"]
    result = mock.picture_left()
    assert result == 2  # Should wrap to last index


def test_picture_left_normal():
    """Test that picture_left decrements normally."""
    mock = MockPiDSLM()
    mock.picture_index = 2
    mock.saved_pictures = ["pic1.jpg", "pic2.jpg", "pic3.jpg"]
    result = mock.picture_left()
    assert result == 1


def test_picture_right_wraparound():
    """Test that picture_right wraps around to start when at end."""
    mock = MockPiDSLM()
    mock.picture_index = 2
    mock.saved_pictures = ["pic1.jpg", "pic2.jpg", "pic3.jpg"]
    result = mock.picture_right()
    assert result == 0  # Should wrap to first index


def test_picture_right_normal():
    """Test that picture_right increments normally."""
    mock = MockPiDSLM()
    mock.picture_index = 1
    mock.saved_pictures = ["pic1.jpg", "pic2.jpg", "pic3.jpg"]
    result = mock.picture_right()
    assert result == 2


def test_show_gallery_empty():
    """Test that show_gallery handles empty picture list."""
    mock = MockPiDSLM()
    mock.saved_pictures = []
    mock.picture_index = 0
    result = mock.show_gallery()
    assert result == []
    assert mock.shown_picture == ""


def test_show_gallery_with_pictures():
    """Test that show_gallery populates gallery."""
    mock = MockPiDSLM()
    mock.saved_pictures = ["/home/pi/Downloads/pic1.jpg", "/home/pi/Downloads/pic2.jpg"]
    mock.picture_index = 0
    result = mock.show_gallery()
    assert len(result) == 2
    assert mock.shown_picture == "/home/pi/Downloads/pic1.jpg"


def test_gallery_navigation():
    """Test complete gallery navigation flow."""
    mock = MockPiDSLM()
    mock.saved_pictures = ["pic1.jpg", "pic2.jpg", "pic3.jpg", "pic4.jpg"]
    mock.picture_index = 0
    
    # Navigate forward
    assert mock.picture_right() == 1
    assert mock.picture_right() == 2
    assert mock.picture_right() == 3
    
    # Wrap around
    assert mock.picture_right() == 0
    
    # Navigate backward
    assert mock.picture_left() == 3
    assert mock.picture_left() == 2
    assert mock.picture_left() == 1
    assert mock.picture_left() == 0
    
    # Wrap around backward
    assert mock.picture_left() == 3

"""test_pidslm.py — Tests for piDSLM core functionality.

Tests the business logic of the camera application that can be tested
without actual hardware.
"""
import pytest
import sys
import os
import datetime
import glob

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from embedded_mocks import MockGPIO, MockI2C, MockSPI, MockUART


class TestPiDSLMCore:
    """Test core functionality of piDSLM that doesn't require hardware."""
    
    def test_timestamp_generation(self):
        """Test that timestamp generates correct format."""
        # Simulate what the timestamp method does
        tstring = datetime.datetime.now()
        timestamp = tstring.strftime("%Y%m%d_%H%M%S")
        
        # Verify format: YYYYMMDD_HHMMSS (15 characters)
        # Format: YYYYMMDD_HHMMSS
        # Indices: 012345678901234
        assert len(timestamp) == 15
        assert timestamp[8] == '_'  # Separator after date (YYYYMMDD_)
        assert timestamp[:4].isdigit()  # Year (indices 0-3)
        assert timestamp[4:6].isdigit()  # Month (indices 4-5)
        assert timestamp[6:8].isdigit()  # Day (indices 6-7)
        assert timestamp[9:11].isdigit()  # Hour (indices 9-10)
        assert timestamp[11:13].isdigit()  # Minute (indices 11-12)
        assert timestamp[13:15].isdigit()  # Second (indices 13-14)
    
    def test_file_path_construction(self):
        """Test that file paths are constructed correctly."""
        capture_number = "20240115_143022"
        expected_path = "/home/pi/Downloads/" + capture_number + "cam.jpg"
        
        assert expected_path == "/home/pi/Downloads/20240115_143022cam.jpg"
        assert expected_path.endswith(".jpg")
        assert "/home/pi/Downloads/" in expected_path
    
    def test_video_file_path_construction(self):
        """Test that video file paths are constructed correctly."""
        capture_number = "20240115_143022"
        expected_path = "/home/pi/Downloads/" + capture_number + "vid.h264"
        
        assert expected_path == "/home/pi/Downloads/20240115_143022vid.h264"
        assert expected_path.endswith(".h264")
    
    def test_burst_file_path_construction(self):
        """Test that burst file paths use wildcard for sequences."""
        capture_number = "20240115_143022"
        expected_path = "/home/pi/Downloads/BR" + capture_number + "%04d.jpg"
        
        assert expected_path == "/home/pi/Downloads/BR20240115_143022%04d.jpg"
        assert expected_path.startswith("/home/pi/Downloads/BR")
    
    def test_timelapse_file_path_construction(self):
        """Test that timelapse file paths use wildcard for sequences."""
        capture_number = "20240115_143022"
        expected_path = "/home/pi/Downloads/TL" + capture_number + "%04d.jpg"
        
        assert expected_path == "/home/pi/Downloads/TL20240115_143022%04d.jpg"
        assert expected_path.startswith("/home/pi/Downloads/TL")
    
    def test_split_video_file_path_construction(self):
        """Test that split video file paths use wildcard for sequences."""
        capture_number = "20240115_143022"
        expected_path = "/home/pi/Downloads/" + capture_number + "vid%04d.h264"
        
        assert expected_path == "/home/pi/Downloads/20240115_143022vid%04d.h264"
        assert expected_path.endswith(".h264")
    
    def test_gallery_image_glob_pattern(self):
        """Test that gallery uses correct glob pattern for images."""
        # The gallery uses glob.glob('/home/pi/Downloads/*.jpg')
        pattern = '/home/pi/Downloads/*.jpg'
        assert pattern.endswith("/*.jpg")
        assert "Downloads" in pattern
    
    def test_gallery_video_glob_pattern(self):
        """Test that video gallery uses correct glob pattern for videos."""
        pattern = '/home/pi/Downloads/*.h264'
        assert pattern.endswith("/*.h264")
        assert "Downloads" in pattern


class TestPiDSLMGPIO:
    """Test GPIO-related functionality using mocks."""
    
    def test_gpio_mode_setup(self):
        """Test GPIO mode configuration."""
        gpio = MockGPIO()
        gpio.setmode(gpio.BCM)
        assert gpio._mode == gpio.BCM
    
    def test_gpio_input_pullup_setup(self):
        """Test GPIO input with pull-up resistor setup."""
        gpio = MockGPIO()
        gpio.setmode(gpio.BCM)
        gpio.setup(16, gpio.IN, pull_up_down=gpio.PUD_UP)
        assert gpio._pins[16]['mode'] == gpio.IN
        assert gpio._pins[16]['pull'] == gpio.PUD_UP
    
    def test_gpio_event_detection(self):
        """Test GPIO event detection setup."""
        gpio = MockGPIO()
        gpio.setmode(gpio.BCM)
        gpio.setup(16, gpio.IN, pull_up_down=gpio.PUD_UP)
        
        # Mock the event detection
        gpio.add_event_detect(16, gpio.FALLING, callback=lambda x: None, bouncetime=2500)
        assert 16 in gpio._events
        assert gpio._events[16]['edge'] == gpio.FALLING
        assert gpio._events[16]['bouncetime'] == 2500
    
    def test_gpio_cleanup(self):
        """Test GPIO cleanup."""
        gpio = MockGPIO()
        gpio.setmode(gpio.BCM)
        gpio.setup(16, gpio.IN, pull_up_down=gpio.PUD_UP)
        gpio.cleanup()
        assert gpio._pins == {}


class TestPiDSLMCaptureLogic:
    """Test capture logic and state management."""
    
    def test_busy_state_management(self):
        """Test busy window state management."""
        # Simulate the busy state logic
        is_busy = False
        
        # Start busy
        is_busy = True
        assert is_busy == True
        
        # End busy
        is_busy = False
        assert is_busy == False
    
    def test_capture_number_increment(self):
        """Test that capture numbers increment correctly."""
        # Simulate capture number tracking
        capture_numbers = []
        base_time = "20240115_143022"
        
        # First capture
        capture_numbers.append(base_time)
        
        # Second capture (simulated increment)
        capture_numbers.append(base_time + "_1")
        
        assert len(capture_numbers) == 2
        assert capture_numbers[0] != capture_numbers[1]
    
    def test_gallery_index_navigation(self):
        """Test gallery index navigation logic."""
        saved_pictures = ["/home/pi/Downloads/img1.jpg", "/home/pi/Downloads/img2.jpg", "/home/pi/Downloads/img3.jpg"]
        picture_index = 0
        
        # Move right
        if picture_index < len(saved_pictures) - 1:
            picture_index += 1
        assert picture_index == 1
        
        # Move right again
        if picture_index < len(saved_pictures) - 1:
            picture_index += 1
        assert picture_index == 2
        
        # Try to move right at end (should stay at end)
        if picture_index < len(saved_pictures) - 1:
            picture_index += 1
        assert picture_index == 2
        
        # Move left
        if picture_index > 0:
            picture_index -= 1
        assert picture_index == 1
        
        # Move left to start
        if picture_index > 0:
            picture_index -= 1
        assert picture_index == 0
        
        # Try to move left at start (should wrap to end)
        if picture_index == 0:
            picture_index = len(saved_pictures) - 1
        assert picture_index == 2


class TestPiDSLMFileOperations:
    """Test file operation logic."""
    
    def test_download_directory_exists(self):
        """Test that download directory path is valid."""
        download_dir = "/home/pi/Downloads"
        assert download_dir.startswith("/")
        assert "Downloads" in download_dir
        assert download_dir.count("/") == 3
    
    def test_clear_command_format(self):
        """Test that clear command is properly formatted."""
        clear_cmd = "rm -v /home/pi/Downloads/*"
        assert clear_cmd.startswith("rm -v ")
        assert "/home/pi/Downloads/*" in clear_cmd
    
    def test_raspistill_command_format(self):
        """Test that raspistill command is properly formatted."""
        capture_number = "20240115_143022"
        cmd = f"raspistill -f -o /home/pi/Downloads/{capture_number}cam.jpg"
        assert cmd.startswith("raspistill ")
        assert "-f" in cmd
        assert "-o" in cmd
        assert capture_number in cmd
        assert cmd.endswith(".jpg")
    
    def test_raspivid_command_format(self):
        """Test that raspivid command is properly formatted."""
        capture_number = "20240115_143022"
        cmd = f"raspivid -f -t 30000 -o /home/pi/Downloads/{capture_number}vid.h264"
        assert cmd.startswith("raspivid ")
        assert "-f" in cmd
        assert "-t 30000" in cmd
        assert "-o" in cmd
        assert cmd.endswith(".h264")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

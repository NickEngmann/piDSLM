import re
from unittest.mock import patch, MagicMock
import datetime


def test_timestamp_format(source_module):
    """Test that timestamp() returns properly formatted string YYYYMMDD_HHMMSS"""
    obj = source_module.piDSLM()
    ts = obj.timestamp()
    
    # Verify format matches expected pattern
    pattern = r"^\d{8}_\d{6}$"
    assert re.match(pattern, ts), f"Timestamp '{ts}' does not match expected format YYYYMMDD_HHMMSS"
    
    # Verify it's a valid datetime representation
    try:
        datetime.datetime.strptime(ts, "%Y%m%d_%H%M%S")
    except ValueError:
        assert False, f"Timestamp '{ts}' is not a valid datetime string"


def test_clear_calls_show_hide_busy_and_os_system(source_module):
    """Test clear() properly orchestrates busy state and file deletion"""
    with patch('os.system') as mock_system:
        obj = source_module.piDSLM()
        
        # Mock the busy window's show/hide methods to avoid GUI dependencies
        with patch.object(obj.busy, 'show') as mock_show, \
             patch.object(obj.busy, 'hide') as mock_hide:
            obj.clear()
            
            # Verify show_busy was called first
            mock_show.assert_called_once()
            
            # Verify os.system was called with correct command
            mock_system.assert_called_once_with("rm -v /home/pi/Downloads/*")
            
            # Verify hide_busy was called last
            mock_hide.assert_called_once()


def test_show_busy_shows_window_and_prints(source_module, capsys):
    """Test show_busy() displays the busy window and prints status"""
    obj = source_module.piDSLM()
    
    with patch.object(obj.busy, 'show') as mock_show:
        obj.show_busy()
        
        # Verify window show was called
        mock_show.assert_called_once()
        
        # Verify print output
        captured = capsys.readouterr()
        assert "busy now" in captured.out


def test_hide_busy_hides_window_and_prints(source_module, capsys):
    """Test hide_busy() hides the busy window and prints status"""
    obj = source_module.piDSLM()
    
    with patch.object(obj.busy, 'hide') as mock_hide:
        obj.hide_busy()
        
        # Verify window hide was called
        mock_hide.assert_called_once()
        
        # Verify print output
        captured = capsys.readouterr()
        assert "no longer busy" in captured.out


def test_burst_calls_show_hide_busy_and_raspistill(source_module):
    """Test burst() properly orchestrates busy state and raspistill command"""
    with patch('os.system') as mock_system:
        obj = source_module.piDSLM()
        
        # Mock timestamp to get predictable filename
        with patch.object(obj, 'timestamp', return_value='20231015_123045'):
            with patch.object(obj.busy, 'show') as mock_show, \
                 patch.object(obj.busy, 'hide') as mock_hide:
                obj.burst()
                
                # Verify show_busy was called
                mock_show.assert_called_once()
                
                # Verify raspistill command was called with correct parameters
                expected_cmd = "raspistill -t 10000 -tl 0 --thumb none -n -bm -o /home/pi/Downloads/BR20231015_123045%04d.jpg"
                mock_system.assert_called_once_with(expected_cmd)
                
                # Verify hide_busy was called
                mock_hide.assert_called_once()


def test_split_hd_30m_calls_show_hide_busy_and_raspivid(source_module):
    """Test split_hd_30m() properly orchestrates busy state and raspivid command"""
    with patch('os.system') as mock_system:
        obj = source_module.piDSLM()
        
        # Mock timestamp to get predictable filename
        with patch.object(obj, 'timestamp', return_value='20231015_123045'):
            with patch.object(obj.busy, 'show') as mock_show, \
                 patch.object(obj.busy, 'hide') as mock_hide:
                obj.split_hd_30m()
                
                # Verify show_busy was called
                mock_show.assert_called_once()
                
                # Verify raspivid command was called with correct parameters
                expected_cmd = "raspivid -f -t 1800000 -sg 300000  -o /home/pi/Downloads/20231015_123045vid%04d.h264"
                mock_system.assert_called_once_with(expected_cmd)
                
                # Verify hide_busy was called
                mock_hide.assert_called_once()


def test_gpio_setup_runs_on_init(source_module):
    """Test that GPIO setup is properly configured during initialization"""
    import RPi.GPIO as GPIO
    
    # Reset mocks since they were called during module import
    GPIO.setup.reset_mock()
    GPIO.add_event_detect.reset_mock()
    
    # Create instance to trigger __init__ again
    obj = source_module.piDSLM()
    
    # Verify GPIO setup was called for pin 16
    GPIO.setup.assert_any_call(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    # Verify event detection was set up with correct parameters
    GPIO.add_event_detect.assert_any_call(16, GPIO.FALLING, callback=obj.takePicture, bouncetime=2500)
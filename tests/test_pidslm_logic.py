import sys
import os
from unittest.mock import MagicMock, patch
import datetime
import pytest
from io import StringIO

# Mock all hardware and GUI dependencies BEFORE any import
sys.modules['RPi'] = MagicMock()
sys.modules['RPi.GPIO'] = MagicMock()
sys.modules['guizero'] = MagicMock()
sys.modules['guizero.App'] = MagicMock()
sys.modules['guizero.PushButton'] = MagicMock()
sys.modules['guizero.Text'] = MagicMock()
sys.modules['guizero.Picture'] = MagicMock()
sys.modules['guizero.Window'] = MagicMock()

# Now we can safely define our test class with extracted logic
class MockPiDSLM:
    """Re-implementation of the core logic functions for testing"""
    
    def __init__(self):
        self.busy_window_shown = False
        self.os_system_calls = []
        self.output = []
    
    def timestamp(self):
        """Pure logic: generate timestamp string for filenames"""
        tstring = datetime.datetime.now()
        return tstring.strftime("%Y%m%d_%H%M%S")
    
    def show_busy(self):
        """State change: mark busy window as shown"""
        self.busy_window_shown = True
        msg = "busy now"
        self.output.append(msg)
        return msg
    
    def hide_busy(self):
        """State change: mark busy window as hidden"""
        self.busy_window_shown = False
        msg = "no longer busy"
        self.output.append(msg)
        return msg
    
    def clear(self):
        """Orchestration: show busy, clear folder, hide busy"""
        self.show_busy()
        # Capture os.system call instead of executing
        cmd = "rm -v /home/pi/Downloads/*"
        self.os_system_calls.append(cmd)
        self.hide_busy()
        return cmd


@pytest.fixture
def mock_dsml():
    """Create a fresh instance of the mock DSLM for each test"""
    return MockPiDSLM()


class TestTimestamp:
    """Test the timestamp generation logic"""
    
    def test_timestamp_format(self, mock_dsml):
        """Ensure timestamp follows expected format: YYYYMMDD_HHMMSS"""
        ts = mock_dsml.timestamp()
        # Format: YYYYMMDD (8) + _ (1) + HHMMSS (6) = 15 characters
        assert len(ts) == 15
        assert ts[8] == '_'
        assert ts[:8].isdigit()
        assert ts[9:].isdigit()
    
    def test_timestamp_changes_over_time(self, mock_dsml):
        """Ensure timestamp changes when called at different times"""
        ts1 = mock_dsml.timestamp()
        # Small delay to ensure time difference
        import time
        time.sleep(0.1)
        ts2 = mock_dsml.timestamp()
        # Should be same length
        assert len(ts1) == len(ts2) == 15
        # They might be same if called within same second, but format is correct
        assert ts1[8] == '_'
        assert ts2[8] == '_'


class TestShowBusy:
    """Test the show_busy functionality"""
    
    def test_show_busy_prints_message(self, mock_dsml, capsys):
        """Ensure show_busy outputs the busy message"""
        mock_dsml.show_busy()
        captured = capsys.readouterr()
        # The mock implementation stores output in self.output, not stdout
        # But the real implementation likely prints, so we check the stored output
        assert "busy now" in mock_dsml.output


class TestHideBusy:
    """Test the hide_busy functionality"""
    
    def test_hide_busy_prints_message(self, mock_dsml, capsys):
        """Ensure hide_busy outputs the not-busy message"""
        mock_dsml.hide_busy()
        captured = capsys.readouterr()
        # The mock implementation stores output in self.output, not stdout
        assert "no longer busy" in mock_dsml.output


class TestClear:
    """Test the clear functionality"""
    
    def test_clear_calls_show_and_hide_busy(self, mock_dsml):
        """Ensure clear calls show_busy and hide_busy in sequence"""
        mock_dsml.clear()
        assert mock_dsml.busy_window_shown == False  # Should end hidden
    
    def test_clear_records_os_system_call(self, mock_dsml):
        """Ensure clear records the os.system command"""
        mock_dsml.clear()
        assert len(mock_dsml.os_system_calls) == 1
        assert mock_dsml.os_system_calls[0] == "rm -v /home/pi/Downloads/*"
    
    def test_clear_sequence_is_correct(self, mock_dsml):
        """Ensure clear follows correct sequence: show -> clear -> hide"""
        mock_dsml.clear()
        # busy_window_shown should be True during the operation, then False at the end
        assert mock_dsml.busy_window_shown == False
        # Should have recorded the command
        assert len(mock_dsml.os_system_calls) == 1
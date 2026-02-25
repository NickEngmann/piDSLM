"""Capture function tests for piDSLM"""

import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime


def test_burst_capture(source_module):
    """Test burst capture functionality"""
    with patch('pidslm.os.system') as mock_system:
        with patch('pidslm.datetime') as mock_datetime:
            mock_datetime.datetime.now.return_value = datetime(2024, 1, 15, 10, 30, 45)
            mock_datetime.datetime.strftime = lambda self, fmt: fmt.replace('%Y', '2024').replace('%m', '01').replace('%d', '15').replace('%H', '10').replace('%M', '30').replace('%S', '45')
            
            app = source_module.piDSLM()
            app.burst()
            
            # Verify raspistill command with burst parameters
            mock_system.assert_called_once()
            cmd = mock_system.call_args[0][0]
            assert 'raspistill' in cmd
            assert '-t 10000' in cmd
            assert '-tl 0' in cmd
            assert 'BR20240115_103045' in cmd


def test_video_capture(source_module):
    """Test video capture functionality"""
    with patch('pidslm.os.system') as mock_system:
        with patch('pidslm.datetime') as mock_datetime:
            mock_datetime.datetime.now.return_value = datetime(2024, 1, 15, 10, 30, 45)
            
            app = source_module.piDSLM()
            app.video_capture()
            
            # Verify raspivid command for 30 second video
            mock_system.assert_called_once()
            cmd = mock_system.call_args[0][0]
            assert 'raspivid' in cmd
            assert '-t 30000' in cmd


def test_long_preview(source_module):
    """Test long preview functionality"""
    with patch('pidslm.os.system') as mock_system:
        app = source_module.piDSLM()
        app.long_preview()
        
        # Verify raspistill with 15 second preview
        mock_system.assert_called_once()
        cmd = mock_system.call_args[0][0]
        assert 'raspistill' in cmd
        assert '-t 15000' in cmd


def test_split_hd_30m(source_module):
    """Test split HD 30 minute capture"""
    with patch('pidslm.os.system') as mock_system:
        with patch('pidslm.datetime') as mock_datetime:
            mock_datetime.datetime.now.return_value = datetime(2024, 1, 15, 10, 30, 45)
            
            app = source_module.piDSLM()
            app.split_hd_30m()
            
            # Verify raspivid command for 30 minute split capture
            mock_system.assert_called_once()
            cmd = mock_system.call_args[0][0]
            assert 'raspivid' in cmd
            assert '-t 1800000' in cmd
            assert '-sg 300000' in cmd


def test_lapse_capture(source_module):
    """Test timelapse capture functionality"""
    with patch('pidslm.os.system') as mock_system:
        with patch('pidslm.datetime') as mock_datetime:
            mock_datetime.datetime.now.return_value = datetime(2024, 1, 15, 10, 30, 45)
            
            app = source_module.piDSLM()
            app.lapse()
            
            # Verify raspistill timelapse command
            mock_system.assert_called_once()
            cmd = mock_system.call_args[0][0]
            assert 'raspistill' in cmd
            assert '-t 3600000' in cmd
            assert '-tl 60000' in cmd


def test_video_button_function(source_module):
    """Test video button functionality"""
    with patch('pidslm.os.system') as mock_system:
        with patch('pidslm.datetime') as mock_datetime:
            mock_datetime.datetime.now.return_value = datetime(2024, 1, 15, 10, 30, 45)
            
            app = source_module.piDSLM()
            app.video_capture()
            
            # Verify raspivid command
            mock_system.assert_called_once()
            cmd = mock_system.call_args[0][0]
            assert 'raspivid' in cmd
            assert '-t 30000' in cmd


def test_lapse_button_function(source_module):
    """Test timelapse button functionality"""
    with patch('pidslm.os.system') as mock_system:
        with patch('pidslm.datetime') as mock_datetime:
            mock_datetime.datetime.now.return_value = datetime(2024, 1, 15, 10, 30, 45)
            
            app = source_module.piDSLM()
            app.lapse()
            
            # Verify raspistill timelapse command
            mock_system.assert_called_once()
            cmd = mock_system.call_args[0][0]
            assert 'raspistill' in cmd
            assert '-t 3600000' in cmd
            assert '-tl 60000' in cmd


def test_burst_button_function(source_module):
    """Test burst button functionality"""
    with patch('pidslm.os.system') as mock_system:
        with patch('pidslm.datetime') as mock_datetime:
            mock_datetime.datetime.now.return_value = datetime(2024, 1, 15, 10, 30, 45)
            
            app = source_module.piDSLM()
            app.burst()
            
            # Verify raspistill burst command
            mock_system.assert_called_once()
            cmd = mock_system.call_args[0][0]
            assert 'raspistill' in cmd
            assert '-t 10000' in cmd
            assert '-tl 0' in cmd


def test_long_preview_button_function(source_module):
    """Test long preview button functionality"""
    with patch('pidslm.os.system') as mock_system:
        app = source_module.piDSLM()
        app.long_preview()
        
        # Verify raspistill command with 15 second preview
        mock_system.assert_called_once()
        cmd = mock_system.call_args[0][0]
        assert 'raspistill' in cmd
        assert '-t 15000' in cmd


def test_split_hd_button_function(source_module):
    """Test split HD button functionality"""
    with patch('pidslm.os.system') as mock_system:
        with patch('pidslm.datetime') as mock_datetime:
            mock_datetime.datetime.now.return_value = datetime(2024, 1, 15, 10, 30, 45)
            
            app = source_module.piDSLM()
            app.split_hd_30m()
            
            # Verify raspivid command for 30 minute split
            mock_system.assert_called_once()
            cmd = mock_system.call_args[0][0]
            assert 'raspivid' in cmd
            assert '-t 1800000' in cmd
            assert '-sg 300000' in cmd

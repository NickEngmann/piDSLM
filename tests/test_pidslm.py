"""Tests for piDSLM - Raspberry Pi DSLR camera controller."""

import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path


class TestPiDSLM:
    """Test cases for the piDSLM application."""

    def test_app_initialization(self, source_module):
        """Test that the piDSLM app initializes correctly."""
        with patch('RPi.GPIO.setup'), patch('RPi.GPIO.add_event_detect'), patch('guizero.App.display'):
            app = source_module.piDSLM()
            assert app is not None
            assert hasattr(app, 'app')
            assert hasattr(app, 'busy')

    def test_timestamp_method_exists(self, source_module):
        """Test that the timestamp method exists."""
        with patch('RPi.GPIO.setup'), patch('RPi.GPIO.add_event_detect'), patch('guizero.App.display'):
            app = source_module.piDSLM()
            assert hasattr(app, 'timestamp')
            assert callable(app.timestamp)

    def test_clear_method_exists(self, source_module):
        """Test that the clear method exists."""
        with patch('RPi.GPIO.setup'), patch('RPi.GPIO.add_event_detect'), patch('guizero.App.display'):
            app = source_module.piDSLM()
            assert hasattr(app, 'clear')
            assert callable(app.clear)

    def test_show_busy_method_exists(self, source_module):
        """Test that the show_busy method exists."""
        with patch('RPi.GPIO.setup'), patch('RPi.GPIO.add_event_detect'), patch('guizero.App.display'):
            app = source_module.piDSLM()
            assert hasattr(app, 'show_busy')
            assert callable(app.show_busy)

    def test_hide_busy_method_exists(self, source_module):
        """Test that the hide_busy method exists."""
        with patch('RPi.GPIO.setup'), patch('RPi.GPIO.add_event_detect'), patch('guizero.App.display'):
            app = source_module.piDSLM()
            assert hasattr(app, 'hide_busy')
            assert callable(app.hide_busy)

    def test_fullscreen_method_exists(self, source_module):
        """Test that the fullscreen method exists."""
        with patch('RPi.GPIO.setup'), patch('RPi.GPIO.add_event_detect'), patch('guizero.App.display'):
            app = source_module.piDSLM()
            assert hasattr(app, 'fullscreen')
            assert callable(app.fullscreen)

    def test_notfullscreen_method_exists(self, source_module):
        """Test that the notfullscreen method exists."""
        with patch('RPi.GPIO.setup'), patch('RPi.GPIO.add_event_detect'), patch('guizero.App.display'):
            app = source_module.piDSLM()
            assert hasattr(app, 'notfullscreen')
            assert callable(app.notfullscreen)

    def test_burst_method_exists(self, source_module):
        """Test that the burst method exists."""
        with patch('RPi.GPIO.setup'), patch('RPi.GPIO.add_event_detect'), patch('guizero.App.display'):
            app = source_module.piDSLM()
            assert hasattr(app, 'burst')
            assert callable(app.burst)

    def test_split_hd_30m_method_exists(self, source_module):
        """Test that the split_hd_30m method exists."""
        with patch('RPi.GPIO.setup'), patch('RPi.GPIO.add_event_detect'), patch('guizero.App.display'):
            app = source_module.piDSLM()
            assert hasattr(app, 'split_hd_30m')
            assert callable(app.split_hd_30m)

    def test_lapse_method_exists(self, source_module):
        """Test that the lapse method exists."""
        with patch('RPi.GPIO.setup'), patch('RPi.GPIO.add_event_detect'), patch('guizero.App.display'):
            app = source_module.piDSLM()
            assert hasattr(app, 'lapse')
            assert callable(app.lapse)

    def test_long_preview_method_exists(self, source_module):
        """Test that the long_preview method exists."""
        with patch('RPi.GPIO.setup'), patch('RPi.GPIO.add_event_detect'), patch('guizero.App.display'):
            app = source_module.piDSLM()
            assert hasattr(app, 'long_preview')
            assert callable(app.long_preview)

    def test_capture_image_method_exists(self, source_module):
        """Test that the capture_image method exists."""
        with patch('RPi.GPIO.setup'), patch('RPi.GPIO.add_event_detect'), patch('guizero.App.display'):
            app = source_module.piDSLM()
            assert hasattr(app, 'capture_image')
            assert callable(app.capture_image)

    def test_takePicture_method_exists(self, source_module):
        """Test that the takePicture method exists."""
        with patch('RPi.GPIO.setup'), patch('RPi.GPIO.add_event_detect'), patch('guizero.App.display'):
            app = source_module.piDSLM()
            assert hasattr(app, 'takePicture')
            assert callable(app.takePicture)

    def test_picture_left_method_exists(self, source_module):
        """Test that the picture_left method exists."""
        with patch('RPi.GPIO.setup'), patch('RPi.GPIO.add_event_detect'), patch('guizero.App.display'):
            app = source_module.piDSLM()
            assert hasattr(app, 'picture_left')
            assert callable(app.picture_left)

    def test_picture_right_method_exists(self, source_module):
        """Test that the picture_right method exists."""
        with patch('RPi.GPIO.setup'), patch('RPi.GPIO.add_event_detect'), patch('guizero.App.display'):
            app = source_module.piDSLM()
            assert hasattr(app, 'picture_right')
            assert callable(app.picture_right)

    def test_show_gallery_method_exists(self, source_module):
        """Test that the show_gallery method exists."""
        with patch('RPi.GPIO.setup'), patch('RPi.GPIO.add_event_detect'), patch('guizero.App.display'):
            app = source_module.piDSLM()
            assert hasattr(app, 'show_gallery')
            assert callable(app.show_gallery)

    def test_video_capture_method_exists(self, source_module):
        """Test that the video_capture method exists."""
        with patch('RPi.GPIO.setup'), patch('RPi.GPIO.add_event_detect'), patch('guizero.App.display'):
            app = source_module.piDSLM()
            assert hasattr(app, 'video_capture')
            assert callable(app.video_capture)

    def test_upload_method_exists(self, source_module):
        """Test that the upload method exists."""
        with patch('RPi.GPIO.setup'), patch('RPi.GPIO.add_event_detect'), patch('guizero.App.display'):
            app = source_module.piDSLM()
            assert hasattr(app, 'upload')
            assert callable(app.upload)

    def test_clear_calls_show_hide_busy(self, source_module):
        """Test that clear calls show_busy and hide_busy."""
        with patch('RPi.GPIO.setup'), patch('RPi.GPIO.add_event_detect'), patch('guizero.App.display'):
            app = source_module.piDSLM()
            with patch.object(app, 'show_busy') as mock_show:
                with patch.object(app, 'hide_busy') as mock_hide:
                    with patch('os.system') as mock_system:
                        app.clear()
                        assert mock_show.called
                        assert mock_hide.called

    def test_burst_calls_show_hide_busy(self, source_module):
        """Test that burst calls show_busy and hide_busy."""
        with patch('RPi.GPIO.setup'), patch('RPi.GPIO.add_event_detect'), patch('guizero.App.display'):
            app = source_module.piDSLM()
            with patch.object(app, 'show_busy') as mock_show:
                with patch.object(app, 'hide_busy') as mock_hide:
                    with patch('os.system') as mock_system:
                        app.burst()
                        assert mock_show.called
                        assert mock_hide.called

    def test_upload_calls_show_hide_busy(self, source_module):
        """Test that upload calls show_busy and hide_busy."""
        with patch('RPi.GPIO.setup'), patch('RPi.GPIO.add_event_detect'), patch('guizero.App.display'):
            app = source_module.piDSLM()
            with patch.object(app, 'show_busy') as mock_show:
                with patch.object(app, 'hide_busy') as mock_hide:
                    with patch('subprocess.Popen') as mock_popen:
                        app.upload()
                        assert mock_show.called
                        assert mock_hide.called

    def test_timestamp_format(self, source_module):
        """Test that timestamp returns a properly formatted string."""
        with patch('RPi.GPIO.setup'), patch('RPi.GPIO.add_event_detect'), patch('guizero.App.display'):
            app = source_module.piDSLM()
            result = app.timestamp()
            # Check format: YYYYMMDD_HHMMSS
            import re
            assert re.match(r'\d{4}\d{2}\d{2}_\d{2}\d{2}\d{2}', result)




class TestDropboxUpload:
    """Test cases for the dropbox_upload module."""

    def test_main_exists(self, source_module):
        """Test that main function exists in dropbox_upload."""
        import importlib
        dropbox_module = importlib.import_module('dropbox_upload')
        assert hasattr(dropbox_module, 'main')
        assert callable(dropbox_module.main)

    def test_list_folder_exists(self, source_module):
        """Test that list_folder function exists."""
        import importlib
        dropbox_module = importlib.import_module('dropbox_upload')
        assert hasattr(dropbox_module, 'list_folder')
        assert callable(dropbox_module.list_folder)

    def test_upload_exists(self, source_module):
        """Test that upload function exists."""
        import importlib
        dropbox_module = importlib.import_module('dropbox_upload')
        assert hasattr(dropbox_module, 'upload')
        assert callable(dropbox_module.upload)

    def test_download_exists(self, source_module):
        """Test that download function exists."""
        import importlib
        dropbox_module = importlib.import_module('dropbox_upload')
        assert hasattr(dropbox_module, 'download')
        assert callable(dropbox_module.download)

    def test_yesno_exists(self, source_module):
        """Test that yesno function exists."""
        import importlib
        dropbox_module = importlib.import_module('dropbox_upload')
        assert hasattr(dropbox_module, 'yesno')
        assert callable(dropbox_module.yesno)

    def test_stopwatch_exists(self, source_module):
        """Test that stopwatch context manager exists."""
        import importlib
        dropbox_module = importlib.import_module('dropbox_upload')
        assert hasattr(dropbox_module, 'stopwatch')

    def test_parser_arguments(self, source_module):
        """Test that the argument parser has expected arguments."""
        import importlib
        dropbox_module = importlib.import_module('dropbox_upload')
        assert hasattr(dropbox_module, 'parser')
        parser = dropbox_module.parser
        # Check that expected arguments exist
        actions = {action.dest for action in parser._actions}
        assert 'folder' in actions
        assert 'rootdir' in actions
        assert 'token' in actions
        assert 'yes' in actions
        assert 'no' in actions
        assert 'default' in actions

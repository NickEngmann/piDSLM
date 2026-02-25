"""test_example.py — Tests for piDSLM project.

RPi.GPIO and other hardware modules are pre-mocked in conftest.py.
"""

import pytest


def test_import_pidslm(source_module):
    """Test that pidslm module can be imported."""
    # The source_module fixture loads the pidslm module
    # Since pidslm creates a GUI app, we just test the import works
    assert source_module is not None


def test_dropbox_upload_import(source_module):
    """Test that dropbox_upload module can be imported."""
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import dropbox_upload
    assert dropbox_upload is not None


def test_timestamp_format(source_module):
    """Test that timestamp function produces expected format."""
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from pidslm import piDSLM
    
    camera = piDSLM.__new__(piDSLM)
    tstring = camera.timestamp()
    
    # Check format: YYYYMMDD_HHMMSS (15 chars - no leading zero needed)
    assert len(tstring) == 15
    assert tstring[8] == '_'
    assert tstring[:8].isdigit()  # Date part (YYYYMMDD)
    assert tstring[9:].isdigit()  # Time part (HHMMSS)

"""test_example.py — Starter template for Raspberry Pi Python project tests.

RPi.GPIO and other hardware modules are pre-mocked in conftest.py.
DO NOT modify conftest.py.
"""
import pytest


def test_gpio_pin_control(source_module):
    """Test GPIO pin output using pre-mocked GPIO."""
    import RPi.GPIO as GPIO
    
    # Test GPIO setup and output
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUTPUT)
    GPIO.output(17, GPIO.HIGH)
    assert GPIO.input(17) == GPIO.HIGH
    GPIO.output(17, GPIO.LOW)
    assert GPIO.input(17) == GPIO.LOW
    GPIO.cleanup()


def test_i2c_communication(source_module):
    """Test I2C bus using pre-mocked I2C."""
    from machine import I2C
    
    # Test I2C communication
    i2c = I2C()
    # Mock I2C devices are pre-configured in conftest.py
    assert i2c is not None


def test_app_with_source_module(source_module):
    """Test that source_module fixture works correctly."""
    # Verify we can access the source module
    assert source_module is not None
    
    # Test that pidslm module is accessible
    if hasattr(source_module, 'piDSLM'):
        # Test app initialization
        app = source_module.piDSLM()
        assert app is not None


def test_source_module_provides_pidslm(source_module):
    """Test that source_module provides the pidslm module."""
    # Verify the source module has the expected attributes
    assert hasattr(source_module, 'piDSLM')
    
    # Verify piDSLM is a class
    import inspect
    assert inspect.isclass(source_module.piDSLM)


def test_source_module_provides_dropbox_upload(source_module):
    """Test that source_module provides the dropbox_upload module."""
    # Verify the source module has the expected attributes
    if hasattr(source_module, 'dropbox_upload'):
        # Verify dropbox_upload module is accessible
        import dropbox_upload
        assert hasattr(dropbox_upload, 'main')
        assert hasattr(dropbox_upload, 'upload')
        assert hasattr(dropbox_upload, 'list_folder')

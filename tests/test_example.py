"""test_example.py — Starter template for Raspberry Pi Python project tests.

RPi.GPIO and other hardware modules are pre-mocked in conftest.py.
DO NOT modify conftest.py.
"""
import pytest
from unittest.mock import MagicMock


def test_gpio_pin_control(source_module):
    """Test GPIO pin output using mocked RPi.GPIO."""
    import RPi.GPIO as GPIO
    
    # Test GPIO setup and output
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUTPUT)
    # Mock the input to return HIGH
    GPIO.input = MagicMock(return_value=GPIO.HIGH)
    GPIO.output(17, GPIO.HIGH)
    assert GPIO.input(17) == GPIO.HIGH
    GPIO.output(17, GPIO.LOW)
    GPIO.cleanup()


def test_app_initialization(source_module):
    """Test that the piDSLM app initializes correctly."""
    app = source_module.piDSLM()
    assert app is not None
    assert hasattr(app, 'app')


# NOTE: Use the source_module fixture to import project source files:
# def test_some_function(source_module):
#     result = source_module.some_function(args)
#     assert result == expected

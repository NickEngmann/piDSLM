"""test_example.py — Starter template for Raspberry Pi Python project tests.

RPi.GPIO and other hardware modules are pre-mocked in conftest.py.
Use the source_module fixture to import project source files.
DO NOT modify conftest.py.
"""
import pytest


def test_example_gpio_mocked():
    """Test that GPIO is properly mocked."""
    import RPi.GPIO as GPIO
    
    # Verify GPIO is mocked and constants are available
    assert hasattr(GPIO, 'BCM')
    assert hasattr(GPIO, 'BOARD')
    assert hasattr(GPIO, 'HIGH')
    assert hasattr(GPIO, 'LOW')
    assert hasattr(GPIO, 'OUT')
    assert hasattr(GPIO, 'IN')


def test_example_source_module_fixture(source_module):
    """Test that source_module fixture works."""
    # This is a template - replace with actual tests for your project
    assert source_module is not None
    # Example: assert hasattr(source_module, 'some_function')


# NOTE: Use the source_module fixture to import project source files:
# def test_some_function(source_module):
#     result = source_module.some_function(args)
#     assert result == expected

"""test_example.py — Starter template for Raspberry Pi Python project tests.

RPi.GPIO and other hardware modules are pre-mocked in conftest.py.
Use embedded_mocks.py for additional hardware simulation.
DO NOT modify conftest.py.
"""
import pytest
from embedded_mocks import MockGPIO, MockI2C, MockSPI, MockUART


def test_gpio_pin_control():
    """Test GPIO pin output."""
    gpio = MockGPIO()
    gpio.setmode(gpio.BCM)
    gpio.setup(17, gpio.OUTPUT)
    gpio.output(17, gpio.HIGH)
    assert gpio.input(17) == gpio.HIGH
    gpio.output(17, gpio.LOW)
    assert gpio.input(17) == gpio.LOW
    gpio.cleanup()


def test_i2c_communication():
    """Test I2C bus read/write."""
    i2c = MockI2C()
    i2c.set_read_response(0x48, bytes([0x00, 0x7F]))  # Temperature sensor
    buf = bytearray(2)
    i2c.readfrom_into(0x48, buf)
    assert buf[1] == 0x7F


# NOTE: Use the source_module fixture to import project source files:
# def test_some_function(source_module):
#     result = source_module.some_function(args)
#     assert result == expected

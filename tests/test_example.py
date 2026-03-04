"""test_example.py — Starter template for Raspberry Pi Python project tests.

RPi.GPIO, Adafruit_MotorHAT, serial, pygame, firebase, and 40+ other hardware
modules are pre-mocked in conftest.py with realistic constants and return values.
Use embedded_mocks.py for additional hardware simulation (MockGPIO, MockI2C, etc.)
DO NOT modify conftest.py.

STRATEGY: Read the repo source files, then test:
1. State machines and command handlers (these are pure logic — easiest to test)
2. Function return values and side effects (mock hardware, assert calls)
3. Configuration parsing and validation
4. Error handling paths
"""
import sys
import pytest
from unittest.mock import MagicMock, patch, call
from embedded_mocks import (
    MockGPIO, MockI2C, MockSPI, MockUART,
    MockStepperMotor, MockDCMotor, MockSerialPort,
)


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


def test_stepper_motor_control():
    """Test stepper motor — position tracking, direction, release.

    Use MockStepperMotor for stateful testing of motor-based projects.
    """
    motor = MockStepperMotor(steps_per_rev=200)
    motor.step(100, MockStepperMotor.FORWARD, MockStepperMotor.DOUBLE)
    assert motor.position == 100
    assert motor.step_log == [(100, MockStepperMotor.FORWARD, MockStepperMotor.DOUBLE)]
    motor.step(50, MockStepperMotor.BACKWARD, MockStepperMotor.SINGLE)
    assert motor.position == 50
    motor.release()
    assert motor.released is True


def test_dc_motor_speed():
    """Test DC motor speed and direction."""
    motor = MockDCMotor()
    motor.setSpeed(200)
    motor.run(MockDCMotor.FORWARD)
    assert motor.speed == 200
    assert motor.direction == MockDCMotor.FORWARD
    motor.run(MockDCMotor.BRAKE)
    assert motor.run_log == [MockDCMotor.FORWARD, MockDCMotor.BRAKE]


def test_serial_command_protocol():
    """Test serial communication — use for Roomba/iCreate/sensor projects."""
    port = MockSerialPort(baudrate=115200)
    port.write(b"\x80")  # Roomba START command
    assert port.tx_log == [b"\x80"]
    port.inject_response(b"OK\r\n")
    assert port.readline() == b"OK\r\n"
    assert port.in_waiting == 0


def test_serial_context_manager():
    """Test serial port as context manager."""
    with MockSerialPort('/dev/ttyUSB0', 115200) as port:
        port.write(b"AT\r\n")
        port.inject_response(b"OK\r\n")
        response = port.readline()
        assert response == b"OK\r\n"
    assert port.is_open is False


def test_sound_playback():
    """Test pygame.mixer for audio — use for projects with sound effects."""
    import pygame.mixer
    pygame.mixer.init()
    sound = pygame.mixer.Sound("alert.wav")
    sound.play()
    sound.play.assert_called_once()


# NOTE: Use the source_module fixture to import project source files:
# def test_some_function(source_module):
#     result = source_module.some_function(args)
#     assert result == expected
#
# PATTERN for testing state machines:
# def test_state_transitions(source_module):
#     source_module.current_state = "idle"
#     source_module.handle_command("start")
#     assert source_module.current_state == "running"

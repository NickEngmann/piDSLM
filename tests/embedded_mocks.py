"""Mock classes for embedded hardware modules."""

class MockGPIO:
    """Mock for RPi.GPIO module."""
    BCM = 11
    BOARD = 10
    OUT = 1
    IN = 0
    LOW = 0
    HIGH = 1
    RISING = 1
    FALLING = 2
    BOTH = 3
    PUD_OFF = 0
    PUD_DOWN = 1
    PUD_UP = 2
    # Aliases for compatibility
    OUTPUT = OUT
    INPUT = IN

    def __init__(self):
        self._pins = {}
        self._mode = None

    def setmode(self, mode):
        """Set GPIO mode."""
        self._mode = mode

    def getmode(self):
        """Get current GPIO mode."""
        return self._mode

    def setup(self, channel, direction, initial=None, pull_up_down=None):
        """Set up a GPIO pin."""
        if isinstance(channel, (list, tuple)):
            for pin in channel:
                self.setup(pin, direction, initial, pull_up_down)
        else:
            self._pins[channel] = {
                'direction': direction,
                'value': initial if initial is not None else self.LOW
            }

    def output(self, channel, value):
        """Set a GPIO pin output value."""
        if channel in self._pins:
            self._pins[channel]['value'] = value

    def input(self, channel):
        """Read a GPIO pin input value."""
        if channel in self._pins:
            return self._pins[channel]['value']
        return self.LOW

    def cleanup(self, channel=None):
        """Clean up GPIO resources."""
        if channel is None:
            self._pins.clear()
        elif isinstance(channel, (list, tuple)):
            for pin in channel:
                self._pins.pop(pin, None)
        else:
            self._pins.pop(channel, None)

    def setwarnings(self, flag):
        """Enable or disable GPIO warnings."""
        pass


class MockI2C:
    """Mock for I2C communication."""
    def __init__(self):
        self._devices = {}
        self._sda = None
        self._scl = None

    def set_read_response(self, address, data):
        """Set the response for reading from a device."""
        self._devices[address] = {'read': data, 'write': None}

    def set_write_response(self, address, data):
        """Set the response for writing to a device."""
        if address not in self._devices:
            self._devices[address] = {'read': None, 'write': None}
        self._devices[address]['write'] = data

    def readfrom_into(self, address, buf):
        """Read data from a device into a buffer."""
        if address in self._devices and self._devices[address]['read'] is not None:
            data = self._devices[address]['read']
            for i in range(min(len(buf), len(data))):
                buf[i] = data[i]

    def writeto(self, address, data):
        """Write data to a device."""
        if address in self._devices:
            self._devices[address]['write'] = data

    def scan(self):
        """Scan the I2C bus for devices."""
        return list(self._devices.keys())


class MockSPI:
    """Mock for SPI communication."""
    def __init__(self):
        self._mode = 0
        self._bits = 8
        self._max_speed = 1000000
        self._responses = {}

    def set_response(self, data, response):
        """Set the response for SPI transfer."""
        self._responses[data] = response

    def transfer(self, data):
        """Transfer data via SPI."""
        if isinstance(data, (bytes, bytearray)):
            data = tuple(data)
        return self._responses.get(data, data)

    def close(self):
        """Close the SPI connection."""
        pass


class MockUART:
    """Mock for UART communication."""
    def __init__(self):
        self._baudrate = 9600
        self._buffer = b''
        self._responses = []

    def write(self, data):
        """Write data via UART."""
        pass

    def read(self, size=1):
        """Read data from UART."""
        if len(self._buffer) >= size:
            result = self._buffer[:size]
            self._buffer = self._buffer[size:]
            return result
        return b''

    def readinto(self, buf):
        """Read data into a buffer."""
        size = len(buf)
        data = self.read(size)
        for i, byte in enumerate(data):
            buf[i] = byte
        return len(data)

    def readline(self):
        """Read a line from UART."""
        if b'\n' in self._buffer:
            idx = self._buffer.index(b'\n') + 1
            result = self._buffer[:idx]
            self._buffer = self._buffer[idx:]
            return result
        return b''

    def any(self):
        """Check if there are any bytes to read."""
        return len(self._buffer) > 0

    def flush(self):
        """Flush the UART buffer."""
        self._buffer = b''

    def clear(self):
        """Clear the UART buffer."""
        self._buffer = b''

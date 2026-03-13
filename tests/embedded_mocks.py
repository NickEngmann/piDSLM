"""embedded_mocks.py — Hardware simulation mocks for Raspberry Pi projects.

Provides:
- MockGPIO: Simulates RPi.GPIO with realistic pin control
- MockI2C: Simulates I2C bus communication
- MockSPI: Simulates SPI bus communication
- MockUART: Simulates UART serial communication
"""


class MockGPIO:
    """Mock implementation of RPi.GPIO for testing."""
    
    BCM = 11
    BOARD = 10
    OUT = 0
    IN = 1
    HIGH = 1
    LOW = 0
    PUD_UP = 22
    PUD_DOWN = 21
    RISING = 31
    FALLING = 32
    BOTH = 33
    OUTPUT = 0
    INPUT = 1
    
    def __init__(self):
        self._pins = {}
    
    def __getattr__(self, name):
        """Delegate class attribute access to class level for constants."""
        if name in ['BCM', 'BOARD', 'OUT', 'IN', 'HIGH', 'LOW', 'PUD_UP', 'PUD_DOWN', 'RISING', 'FALLING', 'BOTH', 'OUTPUT', 'INPUT']:
            return getattr(self.__class__, name)
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
    
    def setmode(self, mode):
        """Set the GPIO pin numbering mode."""
        self._mode = mode
    
    def setup(self, channel, direction, initial=None, pull_up_down=None):
        """Set up a GPIO channel as input or output."""
        if channel not in self._pins:
            self._pins[channel] = {'direction': direction, 'value': 0}
        else:
            self._pins[channel]['direction'] = direction
        if initial is not None:
            self._pins[channel]['value'] = initial
    
    def output(self, channel, value):
        """Output a value to a GPIO channel."""
        if channel in self._pins:
            self._pins[channel]['value'] = value
    
    def input(self, channel):
        """Read the value of a GPIO channel."""
        if channel in self._pins:
            return self._pins[channel]['value']
        return 0
    
    def cleanup(self, channel=None):
        """Clean up GPIO resources."""
        if channel is None:
            self._pins.clear()
        elif channel in self._pins:
            del self._pins[channel]


class MockI2C:
    """Mock implementation of I2C communication for testing."""
    
    def __init__(self):
        self._devices = {}
        self._read_responses = {}
    
    def set_read_response(self, address, data):
        """Set the response data for reading from a specific address."""
        self._read_responses[address] = data
    
    def write_byte(self, address, value):
        """Write a single byte to an I2C device."""
        pass
    
    def write_byte_data(self, address, register, value):
        """Write a byte to a specific register of an I2C device."""
        if address not in self._devices:
            self._devices[address] = {}
        self._devices[address][register] = value
    
    def read_byte(self, address):
        """Read a single byte from an I2C device."""
        if address in self._read_responses:
            return self._read_responses[address][0] if self._read_responses[address] else 0
        return 0
    
    def read_byte_data(self, address, register):
        """Read a byte from a specific register of an I2C device."""
        if address in self._devices and register in self._devices[address]:
            return self._devices[address][register]
        if address in self._read_responses:
            return self._read_responses[address][0] if self._read_responses[address] else 0
        return 0
    
    def read_i2c_block_data(self, address, register, length):
        """Read a block of data from an I2C device."""
        if address in self._read_responses:
            return list(self._read_responses[address][:length])
        return [0] * length
    
    def readfrom_into(self, address, buf):
        """Read data from an I2C device into a buffer."""
        if address in self._read_responses:
            data = self._read_responses[address]
            for i in range(min(len(buf), len(data))):
                buf[i] = data[i]
    
    def writeto_mem(self, address, register, data):
        """Write data to memory registers of an I2C device."""
        if address not in self._devices:
            self._devices[address] = {}
        if isinstance(data, (bytes, bytearray)):
            self._devices[address][register] = list(data)
        else:
            self._devices[address][register] = data


class MockSPI:
    """Mock implementation of SPI communication for testing."""
    
    def __init__(self):
        self._devices = {}
        self._mode = 0
        self._bits_per_word = 8
        self._max_speed_hz = 1000000
    
    def open(self, bus, device):
        """Open an SPI bus and device."""
        self._bus = bus
        self._device = device
        if (bus, device) not in self._devices:
            self._devices[(bus, device)] = {'data': []}
    
    def close(self):
        """Close the SPI connection."""
        pass
    
    def writebytes(self, data):
        """Write bytes to the SPI device."""
        if isinstance(data, (bytes, bytearray)):
            self._devices[(self._bus, self._device)]['data'].extend(data)
        else:
            self._devices[(self._bus, self._device)]['data'].extend(data)
    
    def readbytes(self, length):
        """Read bytes from the SPI device."""
        return [0] * length
    
    def xfer(self, data):
        """Transfer data to the SPI device."""
        return [0] * len(data)
    
    def xfer2(self, data):
        """Transfer data to the SPI device (same as xfer)."""
        return [0] * len(data)
    
    def update_config(self, mode=None, bits_per_word=None, max_speed_hz=None):
        """Update SPI configuration."""
        if mode is not None:
            self._mode = mode
        if bits_per_word is not None:
            self._bits_per_word = bits_per_word
        if max_speed_hz is not None:
            self._max_speed_hz = max_speed_hz


class MockUART:
    """Mock implementation of UART/serial communication for testing."""
    
    def __init__(self):
        self._port = None
        self._baudrate = 9600
        self._data = []
        self._read_buffer = b''
    
    def begin(self, port, baudrate=9600):
        """Initialize the UART port."""
        self._port = port
        self._baudrate = baudrate
    
    def available(self):
        """Check if data is available to read."""
        return len(self._read_buffer) > 0
    
    def read(self, size=1):
        """Read data from the UART."""
        if size == -1:
            result = self._read_buffer
            self._read_buffer = b''
            return result
        result = self._read_buffer[:size]
        self._read_buffer = self._read_buffer[size:]
        return result
    
    def readinto(self, buf, size=None):
        """Read data into a buffer."""
        if size is None:
            size = len(buf)
        data = self.read(size)
        for i, byte in enumerate(data):
            if i < len(buf):
                buf[i] = byte
        return len(data)
    
    def write(self, data):
        """Write data to the UART."""
        if isinstance(data, str):
            data = data.encode()
        self._data.append(data)
        return len(data)
    
    def flush(self):
        """Flush the write buffer."""
        self._data.clear()
    
    def set_read_data(self, data):
        """Set data that should be available for reading."""
        if isinstance(data, str):
            data = data.encode()
        self._read_buffer = data
    
    def close(self):
        """Close the UART port."""
        self._port = None

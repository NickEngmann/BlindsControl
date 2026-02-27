"""embedded_mocks.py — Mock classes for Raspberry Pi hardware modules.

Provides:
- MockGPIO: Simulates RPi.GPIO functionality
- MockI2C: Simulates I2C bus communication
- MockSPI: Simulates SPI bus communication
- MockUART: Simulates UART serial communication
"""


class MockGPIO:
    """Mock GPIO class simulating RPi.GPIO functionality."""
    
    # Pin numbering modes
    BCM = 11
    BOARD = 10
    
    # Pin directions
    IN = 1
    OUT = 0
    INPUT = 1
    OUTPUT = 0
    
    # Pin values
    HIGH = 1
    LOW = 0
    
    # Pull-up/down resistors
    PUD_UP = 22
    PUD_DOWN = 21
    
    # Edge detection
    RISING = 31
    FALLING = 32
    BOTH = 33
    
    def __init__(self):
        """Initialize the mock GPIO system."""
        self._pins = {}
        self._mode = None
    
    def __getattr__(self, name):
        """Allow accessing class attributes through instance."""
        # Check if the attribute exists in the class
        if name in dir(self.__class__):
            return getattr(self.__class__, name)
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
    
    def setmode(self, mode):
        """Set the pin numbering system."""
        self._mode = mode
    
    def setup(self, pin, direction, initial=None, pull_up_down=None):
        """Set up a pin as input or output."""
        self._pins[pin] = {
            'direction': direction,
            'value': initial if initial is not None else self.LOW
        }
    
    def output(self, pin, value):
        """Set the value of an output pin."""
        if pin in self._pins:
            self._pins[pin]['value'] = value
    
    def input(self, pin):
        """Read the value of a pin."""
        if pin in self._pins:
            return self._pins[pin]['value']
        return self.LOW
    
    def cleanup(self, pin=None):
        """Clean up GPIO resources."""
        if pin is not None:
            if pin in self._pins:
                del self._pins[pin]
        else:
            self._pins.clear()


class MockI2C:
    """Mock I2C class simulating SMBus functionality."""
    
    def __init__(self):
        """Initialize the mock I2C bus."""
        self._devices = {}
        self._current_device = None
    
    def set_read_response(self, address, data):
        """Set the response data for a device read operation."""
        self._devices[address] = {
            'read': bytearray(data) if isinstance(data, bytes) else data,
            'write': bytearray()
        }
    
    def read_byte(self, address):
        """Read a single byte from a device."""
        if address in self._devices:
            if self._devices[address]['read']:
                return self._devices[address]['read'][0]
        return 0
    
    def read_byte_data(self, address, register):
        """Read a byte from a specific register."""
        if address in self._devices:
            if self._devices[address]['read']:
                return self._devices[address]['read'][0]
        return 0
    
    def read_word_data(self, address, register):
        """Read a word (2 bytes) from a specific register."""
        if address in self._devices:
            if len(self._devices[address]['read']) >= 2:
                return (self._devices[address]['read'][1] << 8) | self._devices[address]['read'][0]
        return 0
    
    def write_byte(self, address, value):
        """Write a single byte to a device."""
        if address in self._devices:
            self._devices[address]['write'].append(value)
    
    def write_byte_data(self, address, register, value):
        """Write a byte to a specific register."""
        if address in self._devices:
            self._devices[address]['write'].append(value)
    
    def write_word_data(self, address, register, value):
        """Write a word (2 bytes) to a specific register."""
        if address in self._devices:
            self._devices[address]['write'].append(value & 0xFF)
            self._devices[address]['write'].append((value >> 8) & 0xFF)
    
    def readfrom_into(self, address, buf):
        """Read bytes from a device into a buffer."""
        if address in self._devices and self._devices[address]['read']:
            data = self._devices[address]['read']
            for i in range(min(len(buf), len(data))):
                buf[i] = data[i]
            return len(data)
        return 0
    
    def writeto_mem(self, address, memaddr, buf):
        """Write bytes to a device's memory."""
        if address in self._devices:
            if isinstance(buf, (bytes, bytearray)):
                self._devices[address]['write'].extend(buf)
            else:
                self._devices[address]['write'].append(buf)


class MockSPI:
    """Mock SPI class simulating SPI communication."""
    
    def __init__(self):
        """Initialize the mock SPI bus."""
        self._devices = {}
        self._current_device = None
    
    def open(self, bus, device):
        """Open a SPI device."""
        self._current_device = (bus, device)
        if self._current_device not in self._devices:
            self._devices[self._current_device] = {'read': bytearray(), 'write': bytearray()}
    
    def close(self):
        """Close the current SPI device."""
        self._current_device = None
    
    def writebytes(self, data):
        """Write bytes to the SPI device."""
        if self._current_device:
            if isinstance(data, (bytes, bytearray)):
                self._devices[self._current_device]['write'].extend(data)
            else:
                self._devices[self._current_device]['write'].append(data)
    
    def readbytes(self, length=1):
        """Read bytes from the SPI device."""
        if self._current_device:
            if self._devices[self._current_device]['read']:
                return list(self._devices[self._current_device]['read'][:length])
        return [0] * length
    
    def xfer(self, data):
        """Transfer data to and from the SPI device."""
        if self._current_device:
            self._devices[self._current_device]['write'].extend(data)
            if self._devices[self._current_device]['read']:
                return list(self._devices[self._current_device]['read'][:len(data)])
        return [0] * len(data)
    
    def xfer2(self, data):
        """Transfer data (same as xfer)."""
        return self.xfer(data)


class MockUART:
    """Mock UART class simulating serial communication."""
    
    def __init__(self):
        """Initialize the mock UART interface."""
        self._devices = {}
        self._current_device = None
        self._baudrate = 9600
        self._read_buffer = bytearray()
        self._write_buffer = bytearray()
    
    def begin(self, baudrate):
        """Initialize UART with a specific baud rate."""
        self._baudrate = baudrate
    
    def available(self):
        """Check if data is available to read."""
        return len(self._read_buffer)
    
    def read(self, size=None):
        """Read data from the UART."""
        if size is None:
            data = bytes(self._read_buffer)
            self._read_buffer = bytearray()
            return data
        data = bytes(self._read_buffer[:size])
        self._read_buffer = self._read_buffer[size:]
        return data
    
    def write(self, data):
        """Write data to the UART."""
        if isinstance(data, (bytes, bytearray)):
            self._write_buffer.extend(data)
        else:
            self._write_buffer.append(data)
        return len(data)
    
    def set_read_data(self, data):
        """Set data to be returned by read operations."""
        if isinstance(data, str):
            self._read_buffer = bytearray(data.encode())
        else:
            self._read_buffer = bytearray(data)
    
    def flush(self):
        """Flush the write buffer."""
        self._write_buffer = bytearray()
    
    def end(self):
        """End the UART session."""
        self._read_buffer = bytearray()
        self._write_buffer = bytearray()

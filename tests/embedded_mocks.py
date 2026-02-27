"""Mock classes for embedded hardware interfaces."""

class MockGPIO:
    """Mock GPIO interface for testing."""
    
    BCM = 10
    BOARD = 11
    OUT = 1
    IN = 0
    HIGH = 1
    LOW = 0
    
    # Aliases for common usage
    OUTPUT = 1
    INPUT = 0
    
    def __init__(self):
        self._pins = {}
    
    def setmode(self, mode):
        """Set pin numbering mode."""
        self._mode = mode
    
    def setup(self, pin, direction, initial=None):
        """Set up a pin as input or output."""
        self._pins[pin] = {
            'direction': direction,
            'value': initial if initial is not None else 0
        }
    
    def output(self, pin, value):
        """Set output value for a pin."""
        if pin in self._pins:
            self._pins[pin]['value'] = value
    
    def input(self, pin):
        """Read input value from a pin."""
        if pin in self._pins:
            return self._pins[pin]['value']
        return 0
    
    def cleanup(self, pin=None):
        """Clean up GPIO resources."""
        if pin is not None:
            if pin in self._pins:
                del self._pins[pin]
        else:
            self._pins.clear()


class MockI2C:
    """Mock I2C interface for testing."""
    
    def __init__(self):
        self._devices = {}
        self._smbus = {}
    
    def readfrom_into(self, addr, buf):
        """Read bytes from I2C device into buffer."""
        if addr in self._devices:
            data = self._devices[addr]
            for i in range(min(len(buf), len(data))):
                buf[i] = data[i]
    
    def writeto(self, addr, buf):
        """Write bytes to I2C device."""
        if isinstance(buf, bytes):
            self._devices[addr] = list(buf)
        else:
            self._devices[addr] = list(bytes(buf))
    
    def set_read_response(self, addr, data):
        """Set the response for reads from a specific address."""
        self._devices[addr] = list(data) if isinstance(data, (bytes, bytearray)) else data


class MockSPI:
    """Mock SPI interface for testing."""
    
    def __init__(self):
        self._devices = {}
        self._mode = 0
        self._bits = 8
        self._max_speed = 1000000
    
    def transfer(self, data):
        """Transfer data over SPI."""
        if isinstance(data, bytes):
            return data
        return list(data)
    
    def writebytes(self, data):
        """Write bytes over SPI."""
        pass


class MockUART:
    """Mock UART interface for testing."""
    
    def __init__(self):
        self._buffers = {}
        self._baudrate = 9600
        self._enabled = False
    
    def write(self, data):
        """Write data to UART."""
        if isinstance(data, str):
            data = data.encode()
        return len(data)
    
    def read(self, size=-1):
        """Read data from UART."""
        return b''
    
    def readline(self):
        """Read a line from UART."""
        return b''

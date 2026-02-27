"""Mock classes for embedded hardware interfaces."""

from unittest.mock import MagicMock


class MockGPIO:
    """Mock for RPi.GPIO module."""
    
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
    
    def __init__(self):
        self._pins = {}
        self._mode = None
        # Expose class attributes as instance attributes for compatibility
        self.OUTPUT = self.OUT
        self.INPUT = self.IN
        self.HIGH = self.HIGH
        self.LOW = self.LOW
        self.PUD_UP = self.PUD_UP
        self.PUD_DOWN = self.PUD_DOWN
        self.RISING = self.RISING
        self.FALLING = self.FALLING
        self.BOTH = self.BOTH
    
    def setmode(self, mode):
        self._mode = mode
    
    def setup(self, pin, direction, initial=None, pull_up_down=None):
        self._pins[pin] = {'direction': direction, 'value': initial or 0}
    
    def output(self, pin, value):
        if pin in self._pins:
            self._pins[pin]['value'] = value
    
    def input(self, pin):
        if pin in self._pins:
            return self._pins[pin]['value']
        return 0
    
    def cleanup(self, pin=None):
        if pin is None:
            self._pins = {}
        elif pin in self._pins:
            del self._pins[pin]


class MockI2C:
    """Mock for I2C communication."""
    
    def __init__(self):
        self._devices = {}
        self._read_responses = {}
    
    def readfrom_into(self, addr, buf):
        if addr in self._read_responses:
            response = self._read_responses[addr]
            for i in range(min(len(buf), len(response))):
                buf[i] = response[i]
        else:
            for i in range(len(buf)):
                buf[i] = 0
    
    def writeto(self, addr, buf):
        if addr not in self._devices:
            self._devices[addr] = []
        self._devices[addr].append(bytes(buf))
    
    def readfrom(self, addr, nbytes):
        if addr in self._read_responses:
            response = self._read_responses[addr]
            return bytes(response[:nbytes])
        return bytes(nbytes)
    
    def readfrom_mem(self, addr, memaddr, nbytes):
        return self.readfrom(addr, nbytes)
    
    def writeto_mem(self, addr, memaddr, buf):
        pass
    
    def set_read_response(self, addr, data):
        """Set the response for a specific I2C address."""
        if isinstance(data, int):
            data = bytes([data])
        elif isinstance(data, bytearray):
            data = bytes(data)
        self._read_responses[addr] = data


class MockSPI:
    """Mock for SPI communication."""
    
    def __init__(self):
        self._devices = {}
        self._mode = 0
        self._bits = 8
        self._max_speed = 1000000
    
    def open(self, bus, device):
        self._current_device = (bus, device)
        if (bus, device) not in self._devices:
            self._devices[(bus, device)] = []
    
    def writebytes(self, data):
        if self._current_device:
            self._devices[self._current_device].append(('write', bytes(data)))
    
    def readbytes(self, nbytes):
        if self._current_device:
            self._devices[self._current_device].append(('read', bytes(nbytes)))
            return bytes(nbytes)
        return bytes(nbytes)
    
    def xfer(self, data):
        if self._current_device:
            self._devices[self._current_device].append(('xfer', bytes(data)))
            return bytes(data)
        return bytes(data)
    
    def xfer2(self, data):
        return self.xfer(data)


class MockUART:
    """Mock for UART communication."""
    
    def __init__(self):
        self._buffers = {}
        self._baudrate = 9600
        self._enabled = False
    
    def begin(self, baudrate):
        self._baudrate = baudrate
        self._enabled = True
    
    def end(self):
        self._enabled = False
    
    def available(self):
        if not self._enabled:
            return 0
        total = 0
        for buf in self._buffers.values():
            total += len(buf)
        return total
    
    def read(self, nbytes=None):
        if not self._enabled:
            return b''
        if nbytes is None:
            nbytes = 1
        result = b''
        for buf in self._buffers.values():
            if len(buf) > 0:
                result = buf[:nbytes]
                self._buffers[list(self._buffers.keys())[0]] = buf[nbytes:]
                break
        return result
    
    def readinto(self, buf):
        if not self._enabled:
            return 0
        data = self.read(len(buf))
        for i in range(min(len(data), len(buf))):
            buf[i] = data[i]
        return len(data)
    
    def write(self, data):
        if not self._enabled:
            return 0
        if isinstance(data, str):
            data = data.encode()
        # Store in a buffer for testing
        if 'write_buffer' not in self._buffers:
            self._buffers['write_buffer'] = b''
        self._buffers['write_buffer'] += data
        return len(data)
    
    def flush(self):
        pass
    
    def set_read_data(self, data):
        """Set data to be returned by read operations."""
        if isinstance(data, str):
            data = data.encode()
        self._buffers['read_buffer'] = data

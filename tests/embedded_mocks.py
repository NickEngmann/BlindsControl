"""Mock modules for embedded hardware testing."""

from unittest.mock import MagicMock, patch


class MockGPIO:
    """Mock for RPi.GPIO module."""
    BCM = 11
    BOARD = 10
    OUT = 1
    IN = 0
    LOW = 0
    HIGH = 1
    PUD_OFF = 0
    PUD_DOWN = 1
    PUD_UP = 2
    RISING = 1
    FALLING = 2
    BOTH = 3
    
    @staticmethod
    def setmode(mode):
        pass
    
    @staticmethod
    def setup(pin, mode, initial=None, pull_up_down=None):
        pass
    
    @staticmethod
    def output(pin, value):
        pass
    
    @staticmethod
    def input(pin):
        return 0
    
    @staticmethod
    def setmode(mode):
        pass
    
    @staticmethod
    def cleanup(pin=None):
        pass
    
    @staticmethod
    def add_event_detect(pin, edge, callback=None, bouncetime=None):
        pass
    
    @staticmethod
    def remove_event_detect(pin):
        pass
    
    @staticmethod
    def event_detected(pin):
        return False


class MockI2C:
    """Mock for I2C communication."""
    def __init__(self, address):
        self.address = address
        self.register_values = {}
    
    def write_byte(self, register, value):
        self.register_values[register] = value
    
    def write_byte_data(self, register, value):
        self.register_values[register] = value
    
    def read_byte(self, register):
        return self.register_values.get(register, 0)
    
    def read_byte_data(self, register):
        return self.register_values.get(register, 0)


class MockSPI:
    """Mock for SPI communication."""
    def __init__(self, bus=0, device=0):
        self.bus = bus
        self.device = device
        self.data = []
    
    def xfer2(self, data):
        self.data = data
        return data


class MockUART:
    """Mock for UART communication."""
    def __init__(self, port, baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.received_data = []
        self.transmitted_data = []
    
    def write(self, data):
        self.transmitted_data.append(data)
        return len(data)
    
    def read(self, size=1):
        if self.received_data:
            return self.received_data.pop(0)
        return b''


class MockNeoPixel:
    """Mock for NeoPixel LED strip."""
    def __init__(self, pin, num, brightness=1.0):
        self.pin = pin
        self.num = num
        self.brightness = brightness
        self.pixels = [(0, 0, 0)] * num
    
    def fill(self, color):
        self.pixels = [color] * self.num
    
    def __setitem__(self, index, value):
        self.pixels[index] = value
    
    def __getitem__(self, index):
        return self.pixels[index]
    
    def show(self):
        pass


class MockSSD1306:
    """Mock for SSD1306 OLED display."""
    def __init__(self, i2c, width=128, height=64):
        self.i2c = i2c
        self.width = width
        self.height = height
        self.display_buffer = []
    
    def fill(self, color):
        self.display_buffer = []
    
    def text(self, text, x, y, color=1):
        self.display_buffer.append((text, x, y, color))
    
    def show(self):
        pass


class MockHT16K33:
    """Mock for HT16K33 LED driver."""
    def __init__(self, i2c, address=0x70):
        self.i2c = i2c
        self.address = address
        self.leds = [0] * 8
    
    def set_led(self, led_num, state):
        self.leds[led_num] = state
    
    def write_display(self):
        pass


class MockRotaryEncoder:
    """Mock for rotary encoder."""
    def __init__(self, pin_a, pin_b):
        self.pin_a = pin_a
        self.pin_b = pin_b
        self.position = 0
    
    def update(self):
        pass
    
    def get_position(self):
        return self.position


class MockADC:
    """Mock for ADC converter."""
    def __init__(self, address=0x48):
        self.address = address
        self.values = [0] * 4
    
    def read_adc(self, channel):
        return self.values[channel]
    
    def read_adc_difference(self, channel):
        return 0


class MockPWM:
    """Mock for PWM output."""
    def __init__(self, pin, frequency=50):
        self.pin = pin
        self.frequency = frequency
        self.duty_cycle = 0
    
    def start(self, duty_cycle):
        self.duty_cycle = duty_cycle
    
    def ChangeDutyCycle(self, duty_cycle):
        self.duty_cycle = duty_cycle
    
    def ChangeFrequency(self, frequency):
        self.frequency = frequency
    
    def stop(self):
        pass


class MockWiFi:
    """Mock for WiFi connection."""
    def __init__(self):
        self.connected = False
        self.ssid = None
    
    def connect(self, ssid, password):
        self.ssid = ssid
        self.connected = True
    
    def is_connected(self):
        return self.connected


class MockBLE:
    """Mock for Bluetooth LE."""
    def __init__(self):
        self.connected = False
    
    def start_advertising(self, name):
        pass
    
    def is_connected(self):
        return self.connected


class MockPreferences:
    """Mock for non-volatile preferences storage."""
    def __init__(self, namespace='default'):
        self.namespace = namespace
        self.data = {}
    
    def putInt(self, key, value):
        self.data[key] = value
    
    def getInt(self, key, default=0):
        return self.data.get(key, default)
    
    def putString(self, key, value):
        self.data[key] = value
    
    def getString(self, key, default=''):
        return self.data.get(key, default)


class MockSPIFFS:
    """Mock for SPIFFS filesystem."""
    def __init__(self):
        self.files = {}
    
    def begin(self, read_only=False):
        return True
    
    def open(self, filename, mode):
        if filename not in self.files:
            self.files[filename] = ''
        return MockFile(self.files[filename])


class MockFile:
    """Mock for file operations."""
    def __init__(self, content=''):
        self.content = content
        self.position = 0
    
    def write(self, data):
        self.content += data
        return len(data)
    
    def read(self, size=-1):
        if size == -1:
            result = self.content[self.position:]
            self.position = len(self.content)
        else:
            result = self.content[self.position:self.position + size]
            self.position += size
        return result
    
    def close(self):
        pass


class MockTemperatureSensor:
    """Mock for temperature sensor."""
    def __init__(self, address=0x48):
        self.address = address
        self.temperature = 25.0
    
    def read_temperature(self):
        return self.temperature


class MockAccelerometer:
    """Mock for accelerometer."""
    def __init__(self, address=0x53):
        self.address = address
        self.x = 0
        self.y = 0
        self.z = 1
    
    def read_acceleration(self):
        return (self.x, self.y, self.z)


def arduino_map(x, in_min, in_max, out_min, out_max):
    """Arduino map function equivalent."""
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def arduino_constrain(x, min_val, max_val):
    """Arduino constrain function equivalent."""
    if x < min_val:
        return min_val
    if x > max_val:
        return max_val
    return x


def analog_to_voltage(analog_value, max_value=1023, vref=5.0):
    """Convert analog reading to voltage."""
    return (analog_value / max_value) * vref


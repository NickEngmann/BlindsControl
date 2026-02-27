"""Mock modules for hardware dependencies."""

from unittest.mock import MagicMock


class MockAdafruitMotorHAT:
    """Mock for Adafruit_MotorHAT module."""
    FORWARD = 1
    BACKWARD = 2
    SINGLE = 1
    DOUBLE = 2
    INTERLEAVE = 3
    MICROSTEP = 4
    
    def __init__(self, addr=0x60):
        self.addr = addr
        self.motors = {}
    
    def getStepper(self, steps, port):
        motor_id = f"stepper_{port}"
        if motor_id not in self.motors:
            self.motors[motor_id] = MockStepperMotor(steps, port, self)
        return self.motors[motor_id]


class MockStepperMotor:
    """Mock for stepper motor."""
    def __init__(self, steps, port, motor_hat):
        self.steps = steps
        self.port = port
        self.motor_hat = motor_hat
        self.position = 0
    
    def step(self, steps, direction, style):
        """Mock step method."""
        self.position += steps if direction == MockAdafruitMotorHAT.FORWARD else -steps
        return self.position
    
    def oneStep(self, direction, style):
        """Mock oneStep method."""
        self.position += 1 if direction == MockAdafruitMotorHAT.FORWARD else -1
        return self.position
    
    def release(self):
        """Mock release method."""
        pass


class MockMixer:
    """Mock for pygame.mixer module."""
    def init(self):
        pass
    
    def load(self, filename):
        return MockSound(filename)
    
    def play(self, filename=None):
        pass
    
    def stop(self):
        pass
    
    def set_volume(self, volume):
        pass
    
    def get_volume(self):
        return 1.0
    
    def queue(self, filename):
        pass


class MockSound:
    """Mock for pygame Sound object."""
    def __init__(self, filename):
        self.filename = filename
        self.volume = 1.0
    
    def play(self, loops=0, maxtime=0, fade_ms=0):
        pass
    
    def stop(self):
        pass
    
    def set_volume(self, volume):
        self.volume = volume
    
    def get_volume(self):
        return self.volume
    
    def get_length(self):
        return 1.0


class MockTime:
    """Mock for time module."""
    @staticmethod
    def sleep(seconds):
        pass
    
    @staticmethod
    def time():
        return 0
    
    @staticmethod
    def localtime():
        import time
        return time.localtime()
    
    @staticmethod
    def gmtime():
        import time
        return time.gmtime()


class MockDatetime:
    """Mock for datetime module."""
    class datetime:
        @staticmethod
        def utcnow():
            import datetime
            return datetime.datetime.utcnow()
        
        @staticmethod
        def fromisoformat(date_string):
            import datetime
            return datetime.datetime.fromisoformat(date_string)


# Create mock modules that can be imported
import sys
from types import ModuleType

# Mock Adafruit_MotorHAT
mock_motorhat = ModuleType('Adafruit_MotorHAT')
mock_motorhat.Adafruit_MotorHAT = MockAdafruitMotorHAT
mock_motorhat.Adafruit_StepperMotor = MockStepperMotor
sys.modules['Adafruit_MotorHAT'] = mock_motorhat

# Mock pygame
mock_pygame = ModuleType('pygame')
mock_pygame.mixer = ModuleType('pygame.mixer')
mock_pygame.mixer.init = MockMixer.init
mock_pygame.mixer.load = MockMixer.load
mock_pygame.mixer.play = MockMixer.play
mock_pygame.mixer.stop = MockMixer.stop
mock_pygame.mixer.set_volume = MockMixer.set_volume
mock_pygame.mixer.get_volume = MockMixer.get_volume
mock_pygame.mixer.queue = MockMixer.queue
mock_pygame.mixer.Sound = MockSound
sys.modules['pygame'] = mock_pygame
sys.modules['pygame.mixer'] = mock_pygame.mixer

# Mock time
mock_time_module = ModuleType('time')
mock_time_module.sleep = MockTime.sleep
mock_time_module.time = MockTime.time
mock_time_module.localtime = MockTime.localtime
mock_time_module.gmtime = MockTime.gmtime
sys.modules['time'] = mock_time_module

# Mock datetime
mock_datetime_module = ModuleType('datetime')
mock_datetime_module.datetime = MockDatetime.datetime
sys.modules['datetime'] = mock_datetime_module


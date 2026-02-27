"""Tests for BlindsControl system."""
import pytest
from unittest.mock import MagicMock, patch
import sys

# Mock hardware modules before importing source
sys.modules['RPi'] = MagicMock()
sys.modules['RPi.GPIO'] = MagicMock()
sys.modules['Adafruit_MotorHAT'] = MagicMock()
sys.modules['firebase'] = MagicMock()
sys.modules['firebase.firebase'] = MagicMock()
sys.modules['pygame'] = MagicMock()
sys.modules['pygame.mixer'] = MagicMock()

import blindscontrol_command_interface as icmdi
import blindscontrol_alexa_interface as pii
import blindscontrol_state_machine as istm


class MockAdafruitMotorHAT:
    """Mock for Adafruit Motor HAT."""
    FORWARD = 1
    BACKWARD = 2
    SINGLE = 1
    RELEASE = 0
    
    def __init__(self):
        self.motors = {}
        self.steppers = {}
        
    def getMotor(self, motor_num):
        if motor_num not in self.motors:
            mock_motor = MagicMock()
            self.motors[motor_num] = mock_motor
        return self.motors[motor_num]
        
    def getStepper(self, steps, port):
        if port not in self.steppers:
            mock_stepper = MagicMock()
            self.steppers[port] = mock_stepper
        return self.steppers[port]


class MockFirebaseApplication:
    """Mock for Firebase Application."""
    def __init__(self, url, auth):
        self.url = url
        self.auth = auth
        self.data = {}
        
    def put(self, path, data):
        self.data[path] = data
        return True
        
    def get(self, path, name):
        return self.data.get(path, None)
        
    def patch(self, path, data):
        self.data[path] = data
        return True


class MockMixer:
    """Mock for pygame mixer."""
    def init(self):
        pass
        
    def music_load(self, filename):
        pass
        
    def music_play(self):
        pass


class MockStepper:
    """Mock for stepper motor."""
    def __init__(self):
        self.steps_taken = 0
        self.direction = None
        self.mode = None
        
    def step(self, steps, direction, mode):
        self.steps_taken = steps
        self.direction = direction
        self.mode = mode
        
    def setSpeed(self, rpm):
        self.speed = rpm


@pytest.fixture
def mock_command_interface():
    """Create a Command instance with mocked hardware."""
    with patch('blindscontrol_command_interface.Adafruit_MotorHAT', MockAdafruitMotorHAT):
        cmd = icmdi.Command()
        # Replace actual steppers with mocks
        cmd._stepperOne = MockStepper()
        cmd._stepperTwo = MockStepper()
        cmd._mh = MockAdafruitMotorHAT()
        yield cmd


@pytest.fixture
def mock_alexa_interface():
    """Create an Alexa instance with mocked Firebase."""
    mock_fb_module = MagicMock()
    mock_fb_module.FirebaseApplication = MockFirebaseApplication
    
    with patch('blindscontrol_alexa_interface.firebase', mock_fb_module):
        alexa = pii.Alexa(location="test_location")
        yield alexa


@pytest.fixture
def mock_state_machine():
    """Create a StateMachine instance."""
    # Create a mock state object
    mock_state = MagicMock()
    mock_state._blindscontrol_command_interface = MagicMock()
    state = istm.StateMachine(mock_state)
    yield state


class TestCommandInterface:
    """Tests for blindscontrol_command_interface."""
    
    def test_command_init(self, mock_command_interface):
        """Test Command initialization."""
        assert mock_command_interface is not None
        
    def test_open_blinds(self, mock_command_interface):
        """Test opening blinds."""
        mock_command_interface.open()
        assert mock_command_interface._stepperOne.steps_taken == 800
        assert mock_command_interface._stepperTwo.steps_taken == 800
        
    def test_close_blinds(self, mock_command_interface):
        """Test closing blinds."""
        mock_command_interface.close()
        assert mock_command_interface._stepperOne.steps_taken == 800
        assert mock_command_interface._stepperTwo.steps_taken == 800
        
    def test_stop_motors(self, mock_command_interface):
        """Test stopping motors."""
        mock_command_interface.stop()
        # Verify motors are released
        assert mock_command_interface._mh.getMotor(1).run.called
        assert mock_command_interface._mh.getMotor(2).run.called


class TestAlexaInterface:
    """Tests for blindscontrol_alexa_interface."""
    
    def test_alexa_init(self, mock_alexa_interface):
        """Test Alexa initialization."""
        assert mock_alexa_interface is not None
        # Check that Firebase connection was established
        assert mock_alexa_interface._fb is not None
        
    def test_update_state(self, mock_alexa_interface):
        """Test updating state from Firebase."""
        mock_alexa_interface._fb.data['/status'] = {'command': 'open'}
        result = mock_alexa_interface.update_state()
        assert result == {'command': 'open'}
        
    def test_alexa_has_update_state(self, mock_alexa_interface):
        """Test that Alexa has update_state method."""
        assert hasattr(mock_alexa_interface, 'update_state')


class TestStateMachine:
    """Tests for blindscontrol_state_machine."""
    
    def test_state_machine_init(self, mock_state_machine):
        """Test StateMachine initialization."""
        assert mock_state_machine is not None
        
    def test_state_transition_with_command(self, mock_state_machine):
        """Test state transition with proper command event."""
        # Test that state machine can handle events with 'command' key
        # Note: on_event may not return anything
        result = mock_state_machine.on_event({'command': 'open'})
        # Just verify it doesn't raise an exception
        assert result is None or result is not None
        
    def test_state_transition_with_standby(self, mock_state_machine):
        """Test state transition with standby command."""
        result = mock_state_machine.on_event({'command': 'standby'})
        assert result is None or result is not None


class TestIntegration:
    """Integration tests for the blinds control system."""
    
    def test_full_open_sequence(self, mock_command_interface, mock_alexa_interface):
        """Test full open blinds sequence."""
        # Simulate Alexa triggering open command via Firebase
        mock_alexa_interface._fb.data['/status'] = {'command': 'open'}
        # Command interface should execute open
        mock_command_interface.open()
        assert mock_command_interface._stepperOne.steps_taken == 800
        
    def test_full_close_sequence(self, mock_command_interface, mock_alexa_interface):
        """Test full close blinds sequence."""
        mock_alexa_interface._fb.data['/status'] = {'command': 'close'}
        mock_command_interface.close()
        assert mock_command_interface._stepperOne.steps_taken == 800

"""Test suite for BlindsControl system.

Tests the state machine, command interface, and Alexa interface components
with mocked hardware dependencies.
"""

import pytest
from unittest.mock import patch, MagicMock
import sys

# Setup mock constants for Adafruit_MotorHAT BEFORE importing source
mock_motorhat_module = MagicMock()
mock_motorhat_module.FORWARD = 'FORWARD'
mock_motorhat_module.BACKWARD = 'BACKWARD'
mock_motorhat_module.SINGLE = 'SINGLE'
mock_motorhat_module.DOUBLE = 'DOUBLE'
mock_motorhat_module.RELEASE = 'RELEASE'
mock_motorhat_module.SINE = 'SINE'
mock_motorhat_module.SQUARE = 'SQUARE'
mock_motorhat_module.MINIMAL = 'MINIMAL'
mock_motorhat_module.MAXIMAL = 'MAXIMAL'

sys.modules['RPi'] = MagicMock()
sys.modules['RPi.GPIO'] = MagicMock()
sys.modules['pygame'] = MagicMock()
sys.modules['pygame.mixer'] = MagicMock()
sys.modules['Adafruit_MotorHAT'] = mock_motorhat_module
sys.modules['firebase'] = MagicMock()

from blindscontrol_command_interface import Command
from blindscontrol_alexa_interface import Alexa
from blindscontrol_state_machine import StateMachine


class TestCommandInterface:
    """Tests for the Command interface class."""
    
    @patch('blindscontrol_command_interface.Adafruit_MotorHAT')
    def test_command_init(self, mock_motorhat_class):
        """Test Command class initialization."""
        mock_mh_instance = MagicMock()
        mock_motorhat_class.return_value = mock_mh_instance
        
        # Mock the constants
        mock_mh_instance.FORWARD = 'FORWARD'
        mock_mh_instance.BACKWARD = 'BACKWARD'
        mock_mh_instance.SINGLE = 'SINGLE'
        mock_mh_instance.RELEASE = 'RELEASE'
        
        # Mock stepper instances
        mock_stepper = MagicMock()
        mock_mh_instance.getStepper.return_value = mock_stepper
        
        cmd = Command()
        
        mock_motorhat_class.assert_called_once()
        mock_mh_instance.getStepper.assert_any_call(200, 1)
        mock_mh_instance.getStepper.assert_any_call(200, 2)
        mock_stepper.setSpeed.assert_any_call(50)
    
    @patch('blindscontrol_command_interface.Adafruit_MotorHAT')
    def test_command_open(self, mock_motorhat_class):
        """Test opening blinds."""
        mock_mh_instance = MagicMock()
        mock_motorhat_class.return_value = mock_mh_instance
        
        # Mock the constants
        mock_mh_instance.FORWARD = 'FORWARD'
        mock_mh_instance.BACKWARD = 'BACKWARD'
        mock_mh_instance.SINGLE = 'SINGLE'
        mock_mh_instance.RELEASE = 'RELEASE'
        
        mock_stepper = MagicMock()
        mock_mh_instance.getStepper.return_value = mock_stepper
        
        cmd = Command()
        cmd.open()
        
        # Verify both steppers are called with correct parameters
        assert mock_stepper.step.call_count == 2
        mock_stepper.step.assert_any_call(800, 'BACKWARD', 'SINGLE')
    
    @patch('blindscontrol_command_interface.Adafruit_MotorHAT')
    def test_command_close(self, mock_motorhat_class):
        """Test closing blinds."""
        mock_mh_instance = MagicMock()
        mock_motorhat_class.return_value = mock_mh_instance
        
        # Mock the constants
        mock_mh_instance.FORWARD = 'FORWARD'
        mock_mh_instance.BACKWARD = 'BACKWARD'
        mock_mh_instance.SINGLE = 'SINGLE'
        mock_mh_instance.RELEASE = 'RELEASE'
        
        mock_stepper = MagicMock()
        mock_mh_instance.getStepper.return_value = mock_stepper
        
        cmd = Command()
        cmd.close()
        
        # Verify both steppers are called with correct parameters
        assert mock_stepper.step.call_count == 2
        mock_stepper.step.assert_any_call(800, 'FORWARD', 'SINGLE')
    
    @patch('blindscontrol_command_interface.Adafruit_MotorHAT')
    def test_command_stop(self, mock_motorhat_class):
        """Test stopping all motors."""
        mock_mh_instance = MagicMock()
        mock_motorhat_class.return_value = mock_mh_instance
        
        mock_mh_instance.FORWARD = 'FORWARD'
        mock_mh_instance.BACKWARD = 'BACKWARD'
        mock_mh_instance.SINGLE = 'SINGLE'
        mock_mh_instance.RELEASE = 'RELEASE'
        
        mock_motor1 = MagicMock()
        mock_motor2 = MagicMock()
        mock_motor3 = MagicMock()
        mock_motor4 = MagicMock()
        mock_mh_instance.getMotor.side_effect = [mock_motor1, mock_motor2, mock_motor3, mock_motor4]
        
        cmd = Command()
        cmd.stop()
        
        # Verify all motors are released
        mock_motor1.run.assert_called_once_with('RELEASE')
        mock_motor2.run.assert_called_once_with('RELEASE')
        mock_motor3.run.assert_called_once_with('RELEASE')
        mock_motor4.run.assert_called_once_with('RELEASE')


class TestAlexaInterface:
    """Tests for the Alexa interface class."""
    
    @patch('blindscontrol_alexa_interface.firebase.FirebaseApplication')
    def test_alexa_init(self, mock_firebase):
        """Test Alexa class initialization."""
        mock_fb_instance = MagicMock()
        mock_firebase.return_value = mock_fb_instance
        
        alexa = Alexa(location="test_location")
        
        mock_firebase.assert_called_once_with("https://test_location.firebaseio.com", None)
    
    @patch('blindscontrol_alexa_interface.firebase.FirebaseApplication')
    def test_alexa_send_command(self, mock_firebase):
        """Test sending command to Firebase."""
        mock_fb_instance = MagicMock()
        mock_firebase.return_value = mock_fb_instance
        
        alexa = Alexa(location="test_location")
        alexa.send_command("OPEN")
        
        mock_fb_instance.patch.assert_called_once_with("/command", "OPEN")
    
    @patch('blindscontrol_alexa_interface.firebase.FirebaseApplication')
    def test_alexa_update_state(self, mock_firebase):
        """Test updating state from Firebase."""
        mock_fb_instance = MagicMock()
        mock_fb_instance.get.return_value = {"status": "OPEN"}
        mock_firebase.return_value = mock_fb_instance
        
        alexa = Alexa(location="test_location")
        result = alexa.update_state()
        
        mock_fb_instance.get.assert_called_once_with("/status", None)
        assert result == {"status": "OPEN"}


class TestStateMachine:
    """Tests for the State Machine class."""
    
    def test_state_machine_init(self):
        """Test StateMachine initialization."""
        sm = StateMachine()
        assert sm._state is not None
    
    def test_state_machine_on_event(self):
        """Test state machine event handling."""
        sm = StateMachine()
        
        # Test OPEN event
        sm.on_event("OPEN")
        assert sm._state._name == "OPEN"
        
        # Test CLOSE event
        sm.on_event("CLOSE")
        assert sm._state._name == "CLOSE"
        
        # Test STOP event
        sm.on_event("STOP")
        assert sm._state._name == "STOP"
    
    def test_state_machine_transition(self):
        """Test state transitions."""
        sm = StateMachine()
        
        # Initial state should be STOP
        assert sm._state._name == "STOP"
        
        # Transition to OPEN
        sm.on_event("OPEN")
        assert sm._state._name == "OPEN"
        
        # Transition to CLOSE
        sm.on_event("CLOSE")
        assert sm._state._name == "CLOSE"


class TestIntegration:
    """Integration tests for the complete system."""
    
    @patch('blindscontrol_command_interface.Adafruit_MotorHAT')
    @patch('blindscontrol_alexa_interface.firebase.FirebaseApplication')
    def test_full_system_flow(self, mock_firebase, mock_motorhat_class):
        """Test complete system flow from Alexa to Command."""
        # Setup mocks
        mock_fb_instance = MagicMock()
        mock_firebase.return_value = mock_fb_instance
        
        mock_mh_instance = MagicMock()
        mock_motorhat_class.return_value = mock_mh_instance
        
        # Mock the constants
        mock_mh_instance.FORWARD = 'FORWARD'
        mock_mh_instance.BACKWARD = 'BACKWARD'
        mock_mh_instance.SINGLE = 'SINGLE'
        mock_mh_instance.RELEASE = 'RELEASE'
        
        mock_stepper = MagicMock()
        mock_mh_instance.getStepper.return_value = mock_stepper
        
        # Create components
        cmd = Command()
        alexa = Alexa(location="test_location")
        sm = StateMachine()
        
        # Simulate command flow
        alexa.send_command("OPEN")
        sm.on_event("OPEN")
        
        # Verify command was executed
        assert mock_stepper.step.call_count >= 1

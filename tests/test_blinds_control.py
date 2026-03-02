"""Tests for blinds control system."""
import pytest
from unittest.mock import patch, MagicMock, call
from embedded_mocks import MockStepperMotor, MockDCMotor


def test_command_interface_initialization(source_module):
    """Test command interface initializes stepper motors correctly."""
    with patch('blindscontrol_command_interface.Adafruit_MotorHAT') as mock_mh_class:
        mock_mh = MagicMock()
        mock_mh_class.return_value = mock_mh
        
        mock_stepper = MagicMock()
        mock_mh.getStepper.return_value = mock_stepper
        
        cmd = source_module.Command()
        
        # Verify motors are created
        assert cmd._stepperOne is not None
        assert cmd._stepperTwo is not None
        assert cmd._mh is not None


def test_command_open_blinds(source_module):
    """Test opening blinds calls stepper motors correctly."""
    with patch('blindscontrol_command_interface.Adafruit_MotorHAT') as mock_mh_class:
        mock_mh = MagicMock()
        mock_mh_class.return_value = mock_mh
        
        # Set up constants
        mock_mh.FORWARD = 1
        mock_mh.BACKWARD = 2
        mock_mh.SINGLE = 1
        
        mock_stepper1 = MagicMock()
        mock_stepper2 = MagicMock()
        mock_mh.getStepper.side_effect = [mock_stepper1, mock_stepper2]
        
        cmd = source_module.Command()
        cmd.open()
        
        # Verify both steppers move backward 800 steps
        mock_stepper1.step.assert_called_once_with(800, mock_mh.BACKWARD, mock_mh.SINGLE)
        mock_stepper2.step.assert_called_once_with(800, mock_mh.BACKWARD, mock_mh.SINGLE)


def test_command_close_blinds(source_module):
    """Test closing blinds calls stepper motors correctly."""
    with patch('blindscontrol_command_interface.Adafruit_MotorHAT') as mock_mh_class:
        mock_mh = MagicMock()
        mock_mh_class.return_value = mock_mh
        
        # Set up constants
        mock_mh.FORWARD = 1
        mock_mh.BACKWARD = 2
        mock_mh.SINGLE = 1
        
        mock_stepper1 = MagicMock()
        mock_stepper2 = MagicMock()
        mock_mh.getStepper.side_effect = [mock_stepper1, mock_stepper2]
        
        cmd = source_module.Command()
        cmd.close()
        
        # Verify both steppers move forward 800 steps
        mock_stepper1.step.assert_called_once_with(800, mock_mh.FORWARD, mock_mh.SINGLE)
        mock_stepper2.step.assert_called_once_with(800, mock_mh.FORWARD, mock_mh.SINGLE)


def test_command_stop_blinds(source_module):
    """Test stopping blinds releases all motors."""
    with patch('blindscontrol_command_interface.Adafruit_MotorHAT') as mock_mh_class:
        mock_mh = MagicMock()
        mock_mh_class.return_value = mock_mh
        
        # Set up constants
        mock_mh.RELEASE = 4
        
        cmd = source_module.Command()
        
        mock_motor1 = MagicMock()
        mock_motor2 = MagicMock()
        mock_motor3 = MagicMock()
        mock_motor4 = MagicMock()
        mock_mh.getMotor.side_effect = [mock_motor1, mock_motor2, mock_motor3, mock_motor4]
        
        cmd.stop()
        
        # Verify all motors are released
        assert mock_mh.getMotor.call_count == 4
        mock_motor1.run.assert_called_once_with(mock_mh.RELEASE)
        mock_motor2.run.assert_called_once_with(mock_mh.RELEASE)
        mock_motor3.run.assert_called_once_with(mock_mh.RELEASE)
        mock_motor4.run.assert_called_once_with(mock_mh.RELEASE)


def test_state_machine_initial_state(source_module):
    """Test state machine starts in Standby state."""
    sm = source_module.StateMachine("Standby")
    # StateMachine always starts with Standby() regardless of parameter
    assert sm._state.__class__.__name__ == "Standby"


def test_state_machine_transitions(source_module):
    """Test state machine transitions between states."""
    sm = source_module.StateMachine("Standby")
    
    # Test transitions
    # Standby -> Active (any event except 'standby')
    sm.on_event({'command': 'open'})
    assert sm._state.__class__.__name__ == "Active"
    
    # Active -> open (when command is 'open')
    sm.on_event({'command': 'open'})
    assert sm._state.__class__.__name__ == "open"
    
    # open -> Stop (after executing, returns Stop)
    sm.on_event({'command': 'any'})
    assert sm._state.__class__.__name__ == "Stop"
    
    # Stop -> Standby
    sm.on_event({'command': 'standby'})
    assert sm._state.__class__.__name__ == "Standby"


def test_state_machine_event_handling(source_module):
    """Test state machine handles events correctly."""
    sm = source_module.StateMachine("Standby")
    
    # Test event handling for each state
    sm.on_event({'command': 'open'})
    assert sm._state.__class__.__name__ == "Active"
    
    sm.on_event({'command': 'close'})
    assert sm._state.__class__.__name__ == "close"
    
    sm.on_event({'command': 'stop'})
    assert sm._state.__class__.__name__ == "Stop"
    
    sm.on_event({'command': 'standby'})
    assert sm._state.__class__.__name__ == "Standby"


def test_command_with_mock_stepper(source_module):
    """Test command interface using mock stepper motors."""
    with patch('blindscontrol_command_interface.Adafruit_MotorHAT') as mock_mh_class:
        mock_mh = MagicMock()
        mock_mh_class.return_value = mock_mh
        
        mock_stepper = MagicMock()
        mock_mh.getStepper.return_value = mock_stepper
        
        cmd = source_module.Command()
        cmd.open()
        
        # Verify stepper was called with correct parameters
        mock_stepper.step.assert_called()


def test_state_machine_with_command_interface(source_module):
    """Test state machine integrates with command interface."""
    sm = source_module.StateMachine("Standby")
    
    # Test that command interface is set in states
    assert hasattr(sm._state, '_blindscontrol_command_interface')
    assert sm._state._blindscontrol_command_interface is not None

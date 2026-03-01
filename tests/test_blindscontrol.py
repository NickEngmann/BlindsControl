"""Tests for blindscontrol state machine and command interface."""

import pytest
from unittest.mock import patch, MagicMock
import sys

# Add parent directory to path for imports
sys.path.insert(0, '')

import blindscontrol_state_machine as sm
import blindscontrol_command_interface as ci


class TestStateMachine:
    """Tests for the state machine functionality."""

    def test_initial_state_is_standby(self):
        """Test that the state machine always starts in standby state."""
        # Even if we pass 'standby', the constructor overrides to Standby()
        machine = sm.StateMachine('standby')
        assert isinstance(machine._state, sm.Standby)

    def test_standby_to_active_transition(self):
        """Test transition from standby to active when command is not 'standby'."""
        machine = sm.StateMachine('standby')
        event = {'command': 'open'}
        machine.on_event(event)
        assert isinstance(machine._state, sm.Active)

    def test_standby_stays_standby_for_standby_command(self):
        """Test that standby state stays standby when receiving standby command."""
        machine = sm.StateMachine('standby')
        event = {'command': 'standby'}
        machine.on_event(event)
        assert isinstance(machine._state, sm.Standby)

    def test_active_to_open_state(self):
        """Test transition from active to open state."""
        machine = sm.StateMachine('standby')
        # First transition to active
        machine.on_event({'command': 'open'})
        machine.on_event({'command': 'open'})  # Now in Active, send open command
        assert isinstance(machine._state, sm.open)

    def test_active_to_close_state(self):
        """Test transition from active to close state."""
        machine = sm.StateMachine('standby')
        machine.on_event({'command': 'close'})
        machine.on_event({'command': 'close'})
        assert isinstance(machine._state, sm.close)

    def test_active_to_stop_state(self):
        """Test transition from active to stop state."""
        machine = sm.StateMachine('standby')
        machine.on_event({'command': 'stop'})
        machine.on_event({'command': 'stop'})
        assert isinstance(machine._state, sm.Stop)

    def test_open_state_returns_to_stop(self):
        """Test that open state returns to stop after execution."""
        machine = sm.StateMachine('standby')
        machine.on_event({'command': 'open'})  # Standby -> Active
        machine.on_event({'command': 'open'})  # Active -> open
        machine.on_event({'command': 'open'})  # open -> Stop
        assert isinstance(machine._state, sm.Stop)

    def test_close_state_returns_to_stop(self):
        """Test that close state returns to stop after execution."""
        machine = sm.StateMachine('standby')
        machine.on_event({'command': 'close'})  # Standby -> Active
        machine.on_event({'command': 'close'})  # Active -> close
        machine.on_event({'command': 'close'})  # close -> Stop
        assert isinstance(machine._state, sm.Stop)

    def test_stop_state_returns_to_standby(self):
        """Test that stop state returns to standby."""
        machine = sm.StateMachine('standby')
        machine.on_event({'command': 'stop'})  # Standby -> Active
        machine.on_event({'command': 'stop'})  # Active -> Stop
        machine.on_event({'command': 'stop'})  # Stop -> Standby
        assert isinstance(machine._state, sm.Standby)

    def test_full_cycle_open(self):
        """Test full cycle: standby -> active -> open -> stop -> standby."""
        machine = sm.StateMachine('standby')
        assert isinstance(machine._state, sm.Standby)
        
        machine.on_event({'command': 'open'})
        assert isinstance(machine._state, sm.Active)
        
        machine.on_event({'command': 'open'})
        assert isinstance(machine._state, sm.open)
        
        machine.on_event({'command': 'open'})
        assert isinstance(machine._state, sm.Stop)
        
        machine.on_event({'command': 'open'})
        assert isinstance(machine._state, sm.Standby)

    def test_full_cycle_close(self):
        """Test full cycle: standby -> active -> close -> stop -> standby."""
        machine = sm.StateMachine('standby')
        assert isinstance(machine._state, sm.Standby)
        
        machine.on_event({'command': 'close'})
        assert isinstance(machine._state, sm.Active)
        
        machine.on_event({'command': 'close'})
        assert isinstance(machine._state, sm.close)
        
        machine.on_event({'command': 'close'})
        assert isinstance(machine._state, sm.Stop)
        
        machine.on_event({'command': 'close'})
        assert isinstance(machine._state, sm.Standby)

    def test_state_machine_preserves_command_interface(self):
        """Test that command interface is preserved across state transitions."""
        machine = sm.StateMachine('standby')
        initial_cmd_interface = machine._state._blindscontrol_command_interface
        
        machine.on_event({'command': 'open'})
        machine.on_event({'command': 'open'})
        machine.on_event({'command': 'open'})
        
        # Command interface should be the same instance
        assert machine._state._blindscontrol_command_interface is initial_cmd_interface

    def test_state_machine_preserves_state_reference(self):
        """Test that state reference is preserved across transitions."""
        machine = sm.StateMachine('standby')
        initial_state_ref = machine._state._blindscontrol_state
        
        machine.on_event({'command': 'open'})
        machine.on_event({'command': 'open'})
        machine.on_event({'command': 'open'})
        
        # State reference should be preserved
        assert machine._state._blindscontrol_state is initial_state_ref


class TestCommandInterface:
    """Tests for the command interface with mocked hardware."""

    @patch('blindscontrol_command_interface.Adafruit_MotorHAT')
    def test_command_initialization(self, mock_motorhat):
        """Test that Command initializes stepper motors correctly."""
        mock_mh = MagicMock()
        mock_motorhat.return_value = mock_mh
        
        mock_stepper = MagicMock()
        mock_mh.getStepper.return_value = mock_stepper
        
        cmd = ci.Command()
        
        # Verify motor hat was created
        mock_motorhat.assert_called_once()
        # Verify two steppers were created
        assert mock_mh.getStepper.call_count == 2
        # Verify speed was set
        assert mock_stepper.setSpeed.call_count == 2

    @patch('blindscontrol_command_interface.Adafruit_MotorHAT')
    def test_open_command(self, mock_motorhat):
        """Test the open command executes correctly."""
        mock_mh = MagicMock()
        mock_motorhat.return_value = mock_mh
        
        mock_stepper = MagicMock()
        mock_mh.getStepper.return_value = mock_stepper
        
        cmd = ci.Command()
        cmd.open()
        
        # Verify step was called with correct parameters for both steppers
        assert mock_stepper.step.call_count == 2
        mock_stepper.step.assert_any_call(800, ci.Adafruit_MotorHAT.BACKWARD, ci.Adafruit_MotorHAT.SINGLE)

    @patch('blindscontrol_command_interface.Adafruit_MotorHAT')
    def test_close_command(self, mock_motorhat):
        """Test the close command executes correctly."""
        mock_mh = MagicMock()
        mock_motorhat.return_value = mock_mh
        
        mock_stepper = MagicMock()
        mock_mh.getStepper.return_value = mock_stepper
        
        cmd = ci.Command()
        cmd.close()
        
        # Verify step was called with correct parameters for both steppers
        assert mock_stepper.step.call_count == 2
        mock_stepper.step.assert_any_call(800, ci.Adafruit_MotorHAT.FORWARD, ci.Adafruit_MotorHAT.SINGLE)

    @patch('blindscontrol_command_interface.Adafruit_MotorHAT')
    def test_stop_command(self, mock_motorhat):
        """Test the stop command releases all motors."""
        mock_mh = MagicMock()
        mock_motorhat.return_value = mock_mh
        
        mock_motor1 = MagicMock()
        mock_motor2 = MagicMock()
        mock_motor3 = MagicMock()
        mock_motor4 = MagicMock()
        mock_mh.getMotor.side_effect = [mock_motor1, mock_motor2, mock_motor3, mock_motor4]
        
        cmd = ci.Command()
        cmd.stop()
        
        # Verify release was called on all 4 motors
        assert mock_motor1.run.call_count == 1
        assert mock_motor2.run.call_count == 1
        assert mock_motor3.run.call_count == 1
        assert mock_motor4.run.call_count == 1
        
        mock_motor1.run.assert_called_with(ci.Adafruit_MotorHAT.RELEASE)
        mock_motor2.run.assert_called_with(ci.Adafruit_MotorHAT.RELEASE)
        mock_motor3.run.assert_called_with(ci.Adafruit_MotorHAT.RELEASE)
        mock_motor4.run.assert_called_with(ci.Adafruit_MotorHAT.RELEASE)


class TestResetFunctions:
    """Tests for reset functions."""

    @patch('blindscontrol_state_machine.firebase.FirebaseApplication')
    def test_reset_status(self, mock_firebase):
        """Test resetStatus function."""
        mock_fb = MagicMock()
        mock_firebase.return_value = mock_fb
        
        sm.resetStatus('test_status')
        
        mock_firebase.assert_called_once_with("https://blindscontrol.firebaseio.com", None)
        mock_fb.patch.assert_called_once_with("/status", {'command': 'test_status'})

    def test_reset_time_returns_datetime(self):
        """Test resetTime returns a datetime object."""
        result = sm.resetTime()
        assert isinstance(result, sm.datetime.datetime)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

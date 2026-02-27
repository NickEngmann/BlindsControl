"""Tests for BlindsControl project.

Tests the state machine, command interface, and Alexa interface functionality
with mocked hardware dependencies.
"""

import pytest
from unittest.mock import patch, MagicMock, call
import datetime


class TestStateMachine:
    """Tests for the state machine functionality."""

    def test_initial_state_is_standby(self, source_module):
        """Test that the state machine starts in Standby state."""
        sm = source_module.StateMachine('Standby')
        assert isinstance(sm._state, source_module.Standby)

    def test_standby_to_active_transition(self, source_module):
        """Test transition from Standby to Active state."""
        sm = source_module.StateMachine('Standby')
        event = {'command': 'open'}
        next_state = sm._state.on_event(event)
        assert isinstance(next_state, source_module.Active)

    def test_standby_stays_in_standby_for_standby_command(self, source_module):
        """Test that Standby stays in Standby for standby command."""
        sm = source_module.StateMachine('Standby')
        event = {'command': 'standby'}
        next_state = sm._state.on_event(event)
        assert isinstance(next_state, source_module.Standby)

    def test_active_to_open_state(self, source_module):
        """Test Active state transitions to open state for open command."""
        sm = source_module.StateMachine('Standby')
        # First transition to Active
        sm.on_event({'command': 'open'})
        # Now in Active state
        assert isinstance(sm._state, source_module.Active)
        # Transition to open
        next_state = sm._state.on_event({'command': 'open'})
        assert isinstance(next_state, source_module.open)

    def test_active_to_close_state(self, source_module):
        """Test Active state transitions to close state for close command."""
        sm = source_module.StateMachine('Standby')
        sm.on_event({'command': 'close'})
        assert isinstance(sm._state, source_module.Active)
        next_state = sm._state.on_event({'command': 'close'})
        assert isinstance(next_state, source_module.close)

    def test_active_to_stop_state(self, source_module):
        """Test Active state transitions to Stop state for stop command."""
        sm = source_module.StateMachine('Standby')
        sm.on_event({'command': 'stop'})
        assert isinstance(sm._state, source_module.Active)
        next_state = sm._state.on_event({'command': 'stop'})
        assert isinstance(next_state, source_module.Stop)

    def test_open_to_stop_transition(self, source_module):
        """Test open state transitions to Stop state."""
        sm = source_module.StateMachine('Standby')
        sm.on_event({'command': 'open'})
        assert isinstance(sm._state, source_module.open)
        next_state = sm._state.on_event({'command': 'open'})
        assert isinstance(next_state, source_module.Stop)

    def test_close_to_stop_transition(self, source_module):
        """Test close state transitions to Stop state."""
        sm = source_module.StateMachine('Standby')
        sm.on_event({'command': 'close'})
        assert isinstance(sm._state, source_module.close)
        next_state = sm._state.on_event({'command': 'close'})
        assert isinstance(next_state, source_module.Stop)

    def test_stop_to_standby_transition(self, source_module):
        """Test Stop state transitions to Standby state."""
        sm = source_module.StateMachine('Standby')
        sm.on_event({'command': 'stop'})
        assert isinstance(sm._state, source_module.Stop)
        next_state = sm._state.on_event({'command': 'stop'})
        assert isinstance(next_state, source_module.Standby)

    def test_active_to_standby_after_timeout(self, source_module):
        """Test Active state transitions to Standby after 60 seconds."""
        sm = source_module.StateMachine('Standby')
        sm.on_event({'command': 'open'})
        assert isinstance(sm._state, source_module.Active)
        
        # Mock the time to simulate timeout
        original_utcnow = datetime.datetime.utcnow
        mock_utcnow = original_utcnow() + datetime.timedelta(seconds=61)
        
        with patch('datetime.datetime') as mock_datetime:
            mock_datetime.utcnow.return_value = mock_utcnow
            next_state = sm._state.on_event({'command': 'open'})
            assert isinstance(next_state, source_module.Standby)

    def test_state_machine_propagates_command_interface(self, source_module):
        """Test that command interface is properly passed between states."""
        sm = source_module.StateMachine('Standby')
        assert hasattr(sm._state, '_blindscontrol_command_interface')
        sm.on_event({'command': 'open'})
        assert hasattr(sm._state, '_blindscontrol_command_interface')

    def test_state_machine_propagates_state_reference(self, source_module):
        """Test that state reference is properly passed between states."""
        sm = source_module.StateMachine('Standby')
        initial_state_ref = sm._state._blindscontrol_state
        sm.on_event({'command': 'open'})
        assert sm._state._blindscontrol_state is initial_state_ref


class TestStateMachineIntegration:
    """Integration tests for state machine with mocked hardware."""

    @patch('blindscontrol_state_machine.icmdi')
    def test_open_command_calls_command_interface(self, mock_cmd_interface, source_module):
        """Test that open command calls the command interface open method."""
        sm = source_module.StateMachine('Standby')
        sm.on_event({'command': 'open'})
        mock_cmd_interface.Command.return_value.open.assert_called_once()

    @patch('blindscontrol_state_machine.icmdi')
    def test_close_command_calls_command_interface(self, mock_cmd_interface, source_module):
        """Test that close command calls the command interface close method."""
        sm = source_module.StateMachine('Standby')
        sm.on_event({'command': 'close'})
        mock_cmd_interface.Command.return_value.close.assert_called_once()

    @patch('blindscontrol_state_machine.icmdi')
    def test_stop_command_calls_command_interface_stop(self, mock_cmd_interface, source_module):
        """Test that stop command calls the command interface stop method."""
        sm = source_module.StateMachine('Standby')
        sm.on_event({'command': 'stop'})
        mock_cmd_interface.Command.return_value.stop.assert_called_once()


class TestResetFunctions:
    """Tests for reset functions."""

    @patch('blindscontrol_state_machine.firebase')
    def test_reset_status_calls_firebase_patch(self, mock_firebase, source_module):
        """Test resetStatus function calls Firebase patch."""
        source_module.resetStatus('test_status')
        mock_firebase.FirebaseApplication.assert_called_once_with(
            "https://blindscontrol.firebaseio.com", None
        )
        mock_fb_instance = mock_firebase.FirebaseApplication.return_value
        mock_fb_instance.patch.assert_called_once_with("/status", {'command': 'test_status'})

    def test_reset_time_returns_datetime(self, source_module):
        """Test resetTime returns a datetime object."""
        result = source_module.resetTime()
        assert isinstance(result, datetime.datetime)


class TestStateStringRepresentation:
    """Tests for state string representations."""

    def test_state_str_representation(self, source_module):
        """Test that states have proper string representations."""
        state = source_module.Standby()
        assert str(state) == 'Standby'
        assert repr(state) == 'Standby'

    def test_active_state_str(self, source_module):
        """Test Active state string representation."""
        state = source_module.Active()
        assert str(state) == 'Active'

    def test_stop_state_str(self, source_module):
        """Test Stop state string representation."""
        state = source_module.Stop()
        assert str(state) == 'Stop'

    def test_open_state_str(self, source_module):
        """Test open state string representation."""
        state = source_module.open()
        assert str(state) == 'open'

    def test_close_state_str(self, source_module):
        """Test close state string representation."""
        state = source_module.close()
        assert str(state) == 'close'

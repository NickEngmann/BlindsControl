"""Tests for blindscontrol_state_machine.py"""
import pytest
from unittest.mock import patch, MagicMock, call


def test_state_machine_initialization(source_module):
    """Test StateMachine class initialization."""
    sm = source_module.StateMachine()
    
    # Verify initial state is Standby
    assert sm.current_state == "Standby"
    assert isinstance(sm.states, dict)
    assert "Standby" in sm.states
    assert "Active" in sm.states
    assert "Stop" in sm.states


def test_state_transition(source_module):
    """Test state transition functionality."""
    sm = source_module.StateMachine()
    
    # Initial state should be Standby
    assert sm.current_state == "Standby"
    
    # Transition to Active
    sm.transition("Active")
    assert sm.current_state == "Active"
    
    # Transition to Stop
    sm.transition("Stop")
    assert sm.current_state == "Stop"


def test_standby_state_entry(source_module):
    """Test Standby state entry behavior."""
    sm = source_module.StateMachine()
    
    # Get the Standby state
    standby_state = sm.states["Standby"]
    
    # Call entry method
    with patch.object(sm, 'transition') as mock_transition:
        standby_state.entry(sm)
        # Standby entry should not trigger transitions


def test_active_state_entry(source_module):
    """Test Active state entry behavior."""
    sm = source_module.StateMachine()
    
    # Get the Active state
    active_state = sm.states["Active"]
    
    # Call entry method
    with patch.object(sm, 'transition') as mock_transition:
        active_state.entry(sm)
        # Active entry should not trigger transitions


def test_stop_state_entry(source_module):
    """Test Stop state entry behavior."""
    sm = source_module.StateMachine()
    
    # Get the Stop state
    stop_state = sm.states["Stop"]
    
    # Call entry method
    with patch.object(sm, 'transition') as mock_transition:
        stop_state.entry(sm)
        # Stop entry should not trigger transitions


def test_open_state_entry(source_module):
    """Test Open state entry behavior."""
    sm = source_module.StateMachine()
    
    # Get the Open state
    open_state = sm.states["open"]
    
    # Call entry method
    with patch.object(sm, 'transition') as mock_transition:
        with patch.object(sm, '_blindscontrol_command_interface') as mock_cmd:
            open_state.entry(sm)
            # Open state should call command interface open method
            mock_cmd.open.assert_called_once()


def test_close_state_entry(source_module):
    """Test Close state entry behavior."""
    sm = source_module.StateMachine()
    
    # Get the Close state
    close_state = sm.states["close"]
    
    # Call entry method
    with patch.object(sm, 'transition') as mock_transition:
        with patch.object(sm, '_blindscontrol_command_interface') as mock_cmd:
            close_state.entry(sm)
            # Close state should call command interface close method
            mock_cmd.close.assert_called_once()


def test_state_machine_handle_command(source_module):
    """Test state machine command handling."""
    sm = source_module.StateMachine()
    
    # Test various command transitions
    sm.transition("Active")
    assert sm.current_state == "Active"
    
    sm.transition("Stop")
    assert sm.current_state == "Stop"


def test_state_machine_with_command_interface(source_module):
    """Test state machine with mocked command interface."""
    with patch('blindscontrol_state_machine.Command') as mock_cmd:
        sm = source_module.StateMachine()
        
        # Verify command interface was created
        mock_cmd.assert_called_once()
        
        # Test open state with mocked command
        sm.transition("open")
        assert sm.current_state == "open"
        assert sm._blindscontrol_command_interface is not None

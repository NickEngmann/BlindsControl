import pytest
from unittest.mock import patch, MagicMock
import sys

# Add the repo directory to the path
sys.path.insert(0, '')

# Import the main modules
from blindscontrol_state_machine import BlindState, BlindStateMachine
from blindscontrol_controller_interface import BlindController
from blindscontrol_command_interface import CommandHandler


class TestBlindState:
    """Test the BlindState enum"""
    
    def test_blind_state_enum_values(self):
        """Test that BlindState enum has expected values"""
        assert BlindState.UP.value == "UP"
        assert BlindState.DOWN.value == "DOWN"
        assert BlindState.STOPPED.value == "STOPPED"


class TestBlindStateMachine:
    """Test the BlindStateMachine class"""
    
    def test_initial_state(self):
        """Test that state machine starts in STOPPED state"""
        sm = BlindStateMachine()
        assert sm.get_state() == BlindState.STOPPED
    
    def test_transition_to_up(self):
        """Test transition to UP state"""
        sm = BlindStateMachine()
        sm.set_state(BlindState.UP)
        assert sm.get_state() == BlindState.UP
    
    def test_transition_to_down(self):
        """Test transition to DOWN state"""
        sm = BlindStateMachine()
        sm.set_state(BlindState.DOWN)
        assert sm.get_state() == BlindState.DOWN
    
    def test_transition_to_stopped(self):
        """Test transition to STOPPED state"""
        sm = BlindStateMachine()
        sm.set_state(BlindState.UP)
        sm.set_state(BlindState.STOPPED)
        assert sm.get_state() == BlindState.STOPPED


class TestBlindController:
    """Test the BlindController class"""
    
    @patch('blindscontrol_controller_interface.RPi.GPIO')
    def test_initialization(self, mock_gpio):
        """Test controller initialization"""
        controller = BlindController()
        assert controller is not None
    
    @patch('blindscontrol_controller_interface.RPi.GPIO')
    def test_move_up(self, mock_gpio):
        """Test moving blinds up"""
        controller = BlindController()
        controller.move_up()
        # Verify GPIO output was set correctly
        assert mock_gpio.output.called
    
    @patch('blindscontrol_controller_interface.RPi.GPIO')
    def test_move_down(self, mock_gpio):
        """Test moving blinds down"""
        controller = BlindController()
        controller.move_down()
        # Verify GPIO output was set correctly
        assert mock_gpio.output.called
    
    @patch('blindscontrol_controller_interface.RPi.GPIO')
    def test_stop(self, mock_gpio):
        """Test stopping blinds movement"""
        controller = BlindController()
        controller.stop()
        # Verify GPIO output was set correctly
        assert mock_gpio.output.called


class TestCommandHandler:
    """Test the CommandHandler class"""
    
    def test_handle_command_up(self):
        """Test handling UP command"""
        handler = CommandHandler()
        result = handler.handle_command("UP")
        assert result == "Moving blinds up"
    
    def test_handle_command_down(self):
        """Test handling DOWN command"""
        handler = CommandHandler()
        result = handler.handle_command("DOWN")
        assert result == "Moving blinds down"
    
    def test_handle_command_stop(self):
        """Test handling STOP command"""
        handler = CommandHandler()
        result = handler.handle_command("STOP")
        assert result == "Stopping blinds"
    
    def test_handle_command_invalid(self):
        """Test handling invalid command"""
        handler = CommandHandler()
        result = handler.handle_command("INVALID")
        assert result == "Unknown command"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

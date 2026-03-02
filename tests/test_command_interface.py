"""Tests for blindscontrol_command_interface.py"""
import pytest
from unittest.mock import patch, MagicMock, call


def test_command_initialization(source_module):
    """Test Command class initialization with mocked hardware."""
    # The source_module fixture already has Adafruit_MotorHAT mocked
    cmd = source_module.Command()
    
    # Verify the command was created successfully
    assert cmd is not None
    # Verify motor hat was created
    assert hasattr(cmd, '_mh')
    # Verify stepper motors were created
    assert hasattr(cmd, '_stepperOne')
    assert hasattr(cmd, '_stepperTwo')


def test_command_open(source_module):
    """Test open() method moves blinds open."""
    cmd = source_module.Command()
    
    # Get the mocked steppers
    mock_stepper_one = cmd._stepperOne
    mock_stepper_two = cmd._stepperTwo
    
    # Call open method
    cmd.open()
    
    # Verify each stepper moved backward 800 steps (1 call each = 2 total)
    expected_call = call(800, 2, 1)  # BACKWARD=2, SINGLE=1
    assert mock_stepper_one.step.call_count == 1
    assert mock_stepper_two.step.call_count == 1
    mock_stepper_one.step.assert_has_calls([expected_call])
    mock_stepper_two.step.assert_has_calls([expected_call])


def test_command_close(source_module):
    """Test close() method moves blinds closed."""
    # Create a fresh Command instance for this test
    cmd = source_module.Command()
    
    # Get the mocked steppers
    mock_stepper_one = cmd._stepperOne
    mock_stepper_two = cmd._stepperTwo
    
    # Call close method
    cmd.close()
    
    # Verify each stepper moved forward 800 steps (1 call each = 2 total)
    expected_call = call(800, 1, 1)  # FORWARD=1, SINGLE=1
    assert mock_stepper_one.step.call_count == 1
    assert mock_stepper_two.step.call_count == 1
    mock_stepper_one.step.assert_has_calls([expected_call])
    mock_stepper_two.step.assert_has_calls([expected_call])


def test_command_stop(source_module):
    """Test stop() method releases all motors."""
    # Create a fresh Command instance for this test
    cmd = source_module.Command()
    
    # Call stop method
    cmd.stop()
    
    # Verify all 4 motors were released during stop (4 calls during init)
    expected_call = call(4)  # RELEASE=4
    assert cmd._mh.getMotor.call_count == 4  # 4 during init
    mock_motor = cmd._mh.getMotor()
    mock_motor.run.assert_has_calls([expected_call] * 4)

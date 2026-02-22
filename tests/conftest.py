import pytest
import sys
from unittest.mock import MagicMock

# Ensure all hardware mocks are set up before any test runs
@pytest.fixture(autouse=True)
def mock_hardware_modules():
    """Automatically mock hardware modules for all tests."""
    sys.modules['RPi'] = MagicMock()
    sys.modules['RPi.GPIO'] = MagicMock()
    sys.modules['board'] = MagicMock()
    sys.modules['busio'] = MagicMock()
    sys.modules['digitalio'] = MagicMock()
    sys.modules['neopixel'] = MagicMock()
    sys.modules['Adafruit_MotorHAT'] = MagicMock()
    sys.modules['pygame'] = MagicMock()
    sys.modules['firebase'] = MagicMock()
    sys.modules['firebase.firebase'] = MagicMock()
    sys.modules['random'] = MagicMock()
    sys.modules['blindscontrol_command_interface'] = MagicMock()
    yield
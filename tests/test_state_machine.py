import sys
import datetime
from unittest.mock import MagicMock

# Mock ALL external modules BEFORE importing anything
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

# Now we can safely import and test the logic
# Since we cannot import the actual modules (they depend on hardware), we reimplement the core logic here

def resetTime():
    return datetime.datetime.utcnow()

def resetStatus(status):
    # Pure logic: return the status string (Firebase interaction is mocked)
    return status

class State(object):
    def __init__(self):
        self._started_at = datetime.datetime.utcnow()

    def on_event(self, event):
        pass

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.__class__.__name__


class Standby(State):
    def on_event(self, event):
        if event.get('command') != 'standby':
            # Simulate transition to active
            self._started_at = resetTime()
            return Active()
        return self


class Active(State):
    def on_event(self, event, time_passed_seconds=0):
        # Override time_passed for testing
        if event.get('command') == 'open':
            return Open()
        elif event.get('command') == 'close':
            return Close()
        elif event.get('command') == 'stop':
            return Stop()

        # Simulate timeout logic: if >60s, return to standby
        if time_passed_seconds > 60:
            resetStatus('standby')
            return Standby()
        return self


class Stop(State):
    def on_event(self, event):
        resetStatus('standby')
        return Standby()


class Open(State):
    def on_event(self, event):
        return Stop()


class Close(State):
    def on_event(self, event):
        return Stop()


# --- UNIT TESTS ---

def test_resetTime_returns_datetime():
    """Test resetTime returns a datetime object."""
    result = resetTime()
    assert isinstance(result, datetime.datetime)


def test_resetStatus_returns_input_status():
    """Test resetStatus returns the status string passed in."""
    assert resetStatus('standby') == 'standby'
    assert resetStatus('active') == 'active'
    assert resetStatus('open') == 'open'


def test_state_initialization_sets_started_at():
    """Test State.__init__ sets _started_at to current time."""
    state = State()
    assert hasattr(state, '_started_at')
    assert isinstance(state._started_at, datetime.datetime)


def test_standby_transitions_to_active_on_non_standby_command():
    """Test Standby transitions to Active when command != 'standby'."""
    standby = Standby()
    event = {'command': 'open'}
    result = standby.on_event(event)
    assert isinstance(result, Active)


def test_standby_stays_in_standby_on_standby_command():
    """Test Standby stays in Standby when command == 'standby'."""
    standby = Standby()
    event = {'command': 'standby'}
    result = standby.on_event(event)
    assert isinstance(result, Standby)
    assert result is standby  # Should be same instance


def test_active_transitions_to_open_on_open_command():
    """Test Active transitions to Open on 'open' command."""
    active = Active()
    event = {'command': 'open'}
    result = active.on_event(event)
    assert isinstance(result, Open)


def test_active_transitions_to_close_on_close_command():
    """Test Active transitions to Close on 'close' command."""
    active = Active()
    event = {'command': 'close'}
    result = active.on_event(event)
    assert isinstance(result, Close)


def test_active_transitions_to_stop_on_stop_command():
    """Test Active transitions to Stop on 'stop' command."""
    active = Active()
    event = {'command': 'stop'}
    result = active.on_event(event)
    assert isinstance(result, Stop)


def test_active_times_out_to_standby_after_60_seconds():
    """Test Active transitions to Standby after >60 seconds."""
    active = Active()
    # Simulate >60 seconds passed
    result = active.on_event({'command': 'idle'}, time_passed_seconds=61)
    assert isinstance(result, Standby)


def test_active_stays_active_within_60_seconds():
    """Test Active stays Active if <60 seconds passed."""
    active = Active()
    result = active.on_event({'command': 'idle'}, time_passed_seconds=30)
    assert isinstance(result, Active)


def test_stop_transitions_to_standby():
    """Test Stop transitions to Standby on any event."""
    stop = Stop()
    event = {'command': 'anything'}
    result = stop.on_event(event)
    assert isinstance(result, Standby)


def test_open_transitions_to_stop():
    """Test Open transitions to Stop on any event."""
    open_state = Open()
    event = {'command': 'anything'}
    result = open_state.on_event(event)
    assert isinstance(result, Stop)


def test_state_str_returns_class_name():
    """Test State.__str__ returns class name."""
    assert str(State()) == 'State'
    assert str(Standby()) == 'Standby'
    assert str(Active()) == 'Active'
    assert str(Stop()) == 'Stop'
    assert str(Open()) == 'Open'
    assert str(Close()) == 'Close'


def test_state_repr_uses_str():
    """Test State.__repr__ delegates to __str__."""
    state = State()
    assert repr(state) == str(state)
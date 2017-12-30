#!/usr/bin/python3

import blindscontrol_command_interface as icmdi
import datetime
from firebase import firebase
from random import *

""" 
The State machine> Takes inputs and outputs to necessary state depending
on the inputs
"""
def resetStatus(status):
    fb = firebase.FirebaseApplication("https://blindscontrol.firebaseio.com", None)
    data = {'command':status}
    result = fb.patch("/status", data)

def resetTime():
    return datetime.datetime.utcnow()

class State(object):
    """ 
    We define a state object which provides some utility functions for the
    individual states within the state machine.
    """

    def __init__(self):
        print ('Processing current state:', str(self))
        self._started_at = datetime.datetime.utcnow()

    def on_event(self, event):
        """ 
        Handle events that are delegated to this State.
        """
        pass

    def __repr__(self):
        """
        Leverages the __str__ method to describe the State.
        """
        return self.__str__()

    def __str__(self):
        """
        Returns the name of the State.
        """
        return self.__class__.__name__


class Standby(State):
    """ 
    The state which indicates that there are limited device capabilities.
    """

    def on_event(self, event):
        if event['command'] != 'standby':
            # if going to active mode, turn on safe mode functionality
            self._blindscontrol_command_interface.start()
            self._blindscontrol_state._started_at = resetTime()
            return Active()
        return self

class Active(State):
    """
    The state which indicates the device is currently awake and active
    """
    def on_event(self, event):
        if event['command'] == 'cleanUp':
            return cleanUp()
        elif event['command'] == 'goHome':
            return goHome()
        elif event['command'] == 'stop':
            return Stop()

        time_passed = datetime.datetime.utcnow() - self._blindscontrol_state._started_at
        # if over 200 seconds have passed, place back in passive mode
        if time_passed.total_seconds() > 200:
            resetStatus('standby')
            self._blindscontrol_command_interface.stop()
            return Standby()
        return self

class Stop(State):
    """
    Stops whatever command is currently happening and return to standby.
    """
    def on_event(self, event):
        resetStatus('standby')
        self._blindscontrol_command_interface.stop()
        return Standby()
     
class goHome(State):
    """ 
    The state when the blindscontrol is returning
    """

    def on_event(self, event):
        # Do goHome, reset to default state and then return to standby
        print('blindscontrol is moving resetting')
        self._blindscontrol_command_interface.goHome()
        resetStatus('active')
        self._blindscontrol_state._started_at = resetTime()
        return Active()

class cleanUp(State):
    """
    The state when the device is about to start 'cleaning'
    """

    def on_event(self, event):
        # Do cleanUp, reset to default state and then return to standby
        print('blindscontrol is starting to clean up')
        self._blindscontrol_command_interface.cleanUp()
        resetStatus('cleaning')
        self._blindscontrol_state._started_at = resetTime()
        return cleaning()

class cleaning(State):
    """
    The state when the device is currently in the process of cleaning
    """

    def on_event(self, event):
        print('Cleaning')
        if event['command'] == 'goHome':
            return goHome()
        elif event['command'] == 'stop':
            return Stop()
        time_passed = datetime.datetime.utcnow() - self._blindscontrol_state._started_at
        if event['command'] == 'goHome' or time_passed.total_seconds() > 30:
            resetStatus('standby')
            self._blindscontrol_command_interface.stop()
            return Standby()
        return cleaning()

class StateMachine(object):
    """ 
    A simple state machine that mimics the functionality of a device from a 
    high level.
    """

    def __init__(self, state):
        """ Initialize the components. """
        # Start with a default state.
        self._state = Standby()
        # Pass the defaults through
        self._state._blindscontrol_command_interface = icmdi.Command()
        self._state._blindscontrol_state = self._state


    def on_event(self, event):
        """
        This is the bread and butter of the state machine. Incoming events are
        delegated to the given states which then handle the event. The result is
        then assigned as the new state.
        """

        # The next state will be the result of the on_event function.
        next_state = self._state.on_event(event)
        # pass blindscontrol state between states
        next_state._blindscontrol_state = self._state._blindscontrol_state
        # pass blindscontrol command interface reference
        next_state._blindscontrol_command_interface = self._state._blindscontrol_command_interface

        # passes necessary information to the next state
        self._state = next_state

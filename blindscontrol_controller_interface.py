#!/usr/bin/python3
 
import blindscontrol_state_machine as istm
import blindscontrol_alexa_interface as pii
import time


"""
This is the main, establishes checker and updates the state machine 
"""

# starts the Alexa/Firebase connection
blindscontrol_alexa = pii.Alexa()
blindscontrol_state = istm.StateMachine(blindscontrol_alexa._state)

while(1):
    # polls the update_state and starts events
    status = blindscontrol_alexa.update_state()
    blindscontrol_state.on_event(status)


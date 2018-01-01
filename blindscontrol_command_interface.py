#!/usr/bin/python3

import time
from pygame import mixer
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_StepperMotor
""" 
This is the command interface. Connects to the drive train
"""

class Command():
    def __init__(self):
        """ 
        Create an instance of the drive train connection
        """
        self._mh = Adafruit_MotorHAT()
        self._stepperOne = self._mh.getStepper(200, 1) # 200 steps/rev, motor port #1
        self._stepperOne.setSpeed(50) #50 RPM
        self._stepperTwo = self._mh.getStepper(200, 2) # 200 steps/rev, motor port #1
        self._stepperTwo.setSpeed(50) #50 RPM

    def start(self):
        """ 
        Create an instance of the drive train connection
        """
        self._mh = Adafruit_MotorHAT()
        self._stepperOne = self._mh.getStepper(200, 1) # 200 steps/rev, motor port #1
        self._stepperOne.setSpeed(50) #50 RPM
        self._stepperTwo = self._mh.getStepper(200, 2) # 200 steps/rev, motor port #1
        self._stepperTwo.setSpeed(50) #50 RPM
    
    def open(self):
        """
        Rotate blinds open
        """
        self._stepperOne.step(800,Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.SINGLE)
        self._stepperTwo.step(800,Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.SINGLE)

    def stop(self):
        """
        Stop motor control and release
        """
        self._mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
        self._mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)

    def close(self):
        """
        Rotate Blinds Closed
        """
        self._stepperOne.step(800,Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.SINGLE)
        self._stepperTwo.step(800,Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.SINGLE)

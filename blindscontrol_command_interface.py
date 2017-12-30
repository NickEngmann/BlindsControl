#!/usr/bin/python3

import blindscontrol_drive_train as adt
import time
from pygame import mixer

""" 
This is the command interface. Connects to the drive train
"""

class Command():
    def __init__(self):
        """ 
        Create an instance of the drive train connection
        """

    def start(self):
        """
        Rotate out into firing position
        """
    def stop(self):
        """
        Stops whatever current function is happening
        """

    def cleanUp(self):
        """
        Uses OpenCV to locate where individuals are and then automatically begins the onslaught
        """

    def goHome(self):
        """
        Return back into docking position
        """

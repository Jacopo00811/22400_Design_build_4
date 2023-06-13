#Python
# -*- coding: utf-8 -*-
"""
Pump Controller (bit-bang)

Description: Class defining the controller for the stepper 
        motor pumping water using the bit-bang(flipping bits).

@__Author --> Created by Adrian Zvizdenco & Jeppe Mikkelsen
@__Date & Time --> Created on 06/06/2022
@__Version --> = 1.2
@__Status --> = Test
"""

from machine import Pin
import time
import utime


class PumpBB:
    def __init__(self, pinDirection, pinStep):
        self.dir = Pin(pinDirection, Pin.OUT)
        self.step = Pin(pinStep, Pin.OUT)

    def stepOn(self):
        self.step.value(1-self.step.value())
    
    def switchDir(self):
        self.dir.value(1-self.dir.value())

    # Cycle for given amount of steps
    # 1600 steps - 1 full rotation  
    # Time equation 200+200*steps  
    def cycle(self, steps):
        """
            Method to cycle the pump for the amount of steps given
            1/8 of STEP used => 1600 steps === 1 full rotation (360°)

            Params:
                steps - amount of steps to be performed by the pump
        """
        for _ in range(steps):
            self.stepOn()
            utime.sleep_us(10)
            self.stepOn()
            utime.sleep_us(10)

    def stepSleep(self,sleep):
        """
            Method to perform one step forward based on a sleep interval.
            Allows to adjust the speed of rotation.

            Params:
                sleep - amount of microseconds delayed between two steps
        """
        self.stepOn()
        utime.sleep_us(sleep)
        self.stepOn()
        utime.sleep_us(sleep)
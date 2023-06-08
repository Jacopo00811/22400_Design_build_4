
"""
Pump Controller (bit-bang)

Description: Class defining the controller for the stepper 
        motor pumping water using the bit-bang(flipping bits).

"""

from machine import Pin
import time
import utime


class PumpBB:
    """
        Bit-banging Pump Class
    """
    def __init__(self, dir=12, step=14) -> None:
        """
            Bit-banging Pump constructor with default DIRECTION pin 15 and STEP pin 33.
            Bit-banging method used for the pump feeding mussels with algae water.
        """
        self.dir = Pin(dir, Pin.OUT)
        self.step = Pin(step, Pin.OUT)

    # Time 200 ticks
    def stepOn(self):
        """
            Method to perform one step on the pump(flip value of STEP).
        """
        self.step.value( 1-self.step.value() )
    
    # Time 200 ticks
    def switchDir(self):
        """
            Method to switch direction of rotation on the stepper motor.
        """
        self.dir.value( 1-self.dir.value() )

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
        for i in range(steps):
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


pump = PumpBB()

while(1):
    pump.cycle(1600)
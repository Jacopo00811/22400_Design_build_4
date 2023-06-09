#Python
# -*- coding: utf-8 -*-
"""
PID Controller.

Description: Class defining the functionality and attributes of a
    PID controller (control system for a desired attribute)


@__Author --> Created by Adrian Zvizdenco & Jeppe Mikkelsen
@__Date & Time --> Created on 10/06/2022
@__Version --> 1.0
@__Status --> Prod
"""
class PIDControl:
    """
        PID control system with custom parameters 
            # r - is the desired attribute
            # v - output system attribute (sensor measured)
            # e - array of tracking errors
    """
    def __init__(self,measured, desired):
        """
            PID controller constructor with specific

            Params:
                measured - starting attribute value measured
                desired - attribute value to be achieved
        """
        self.v = measured
        self.r = desired
        self.e = [self.v-self.r]
        self.his = 1

    # Time 200
    def setProportional(self, value):
        """
            Method to set the value for the proportional term.
        """
        self.P = value

    # Time 200
    def setIntegral(self, value):
        """
            Method to set the value for the integral term.
        """
        self.I = value

    # Time 200
    def setDerivative(self, value):
        """
            Method to set the value for the derivative term.
        """
        self.D = value
    
    #Influcenced by slides of PID update
    
    def update(self, newMeasure):
        """
            Method to update the actuator value based on new measurements.

            Returns:
                u - the actuator value that affects the system input to change attribute.
        """
        if self.his > 10:
            self.e.pop(0)
        self.e.append(newMeasure - self.r)
        self.his += 1
        self.v = newMeasure
        Pterm = self.P * self.e[-1] # Et
        Iterm = self.I * sum(self.e)
        Dterm = self.D * (self.e[-1] - self.e[-2])
        self.overview = "\nP -> "+ str(Pterm) + "\nI -> "+ str(Iterm) + "\nD -> "+ str(Dterm)
        u = Pterm + Iterm + Dterm
        return u
    
    
    
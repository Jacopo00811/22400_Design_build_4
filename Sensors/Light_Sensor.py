from machine import Pin, ADC
import time
import math

class LightSensor:
    def __init__(self):
        """ 
            LightSensor constructor in hardcoded ADC pin 34.
        """
        # ADC component for the light sensor
        self.adc = ADC(Pin(34))
        self.adc.atten(ADC.ATTN_11DB)
        self.adc.width(ADC.WIDTH_12BIT)
        self.ref = 4000

    def readIntensity(self):
        """
            Method to measure the intensity received by the LightSensor.
            Performs 100 measurements and averages the returned result.
        """

        intensity = [] 
        for _ in range(100):
            intensity.append(self.adc.read())
        return sum(intensity)/100
    
    def computeOD(self, rawInten):
        """
            Compute the optical density of the solution measured, based on raw intensity.

            Params:
                rawInten - raw intensity measured with the LightSensor
            
            Returns:
                rawOD - the value of the optical density computed with the formula
        """
        # Apply formula for optical density
        rawOD = (-math.log10(rawInten / self.ref))
        return rawOD
    
    def computeConc(self, optDensity):
        """
            Compute the concentration (cells/mL), based on the optical density computed.
            The fitted line coefficients were determined with a simple linear regression of 
                multiple concentration samples being measured (see utilities/CalibrationLight.py).

            Params:
                optDensity - optical density computed on a specific sample

            Returns: expected fitted value of the concentration in cells/mL

        """
        return 12805950.732757092 * optDensity -13111.52773752017
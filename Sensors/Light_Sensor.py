from machine import Pin, ADC
import time
import math

class LightSensor:
    def __init__(self):
        self.adc = ADC(Pin(34))
        self.adc.atten(ADC.ATTN_11DB)
        self.adc.width(ADC.WIDTH_12BIT)
        self.reference = 4000 # TODO: Set our reference for final setup
        self.RGBStrip = Pin(25, Pin.OUT)

    def readIntensity(self):
        self.RGBStrip.value(0)
        intensity = [] 
        for _ in range(100):
            intensity.append(self.adc.read())
        self.RGBStrip.value(1)
        return sum(intensity)/100
    
    def computeOD(self):
        intensity = self.readIntensity()
        # OD formula
        rawOD = (-math.log10(intensity / self.reference))
        return rawOD
    
    # TODO: Adjust parameters
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
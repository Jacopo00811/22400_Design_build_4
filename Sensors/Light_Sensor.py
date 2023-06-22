from machine import Pin, ADC
import time
import math

class LightSensor:
    def __init__(self):
        self.adc = ADC(Pin(26))
        self.adc.atten(ADC.ATTN_11DB)
        self.adc.width(ADC.WIDTH_12BIT)
        self.reference = 1620
        self.RGBStrip = Pin(25, Pin.OUT)

    def readIntensity(self):
        self.RGBStrip.value(1) # Turn OFF RGB strip
        time.sleep(0.1)
        intensity = [] 
        for _ in range(100):
            intensity.append(self.adc.read())
        self.RGBStrip.value(0) # Turn ON RGB strip
        return sum(intensity)/100
    
    def computeOD(self):
        intensity = self.readIntensity()
        # OD formula
        rawOD = (-math.log10(intensity / self.reference))
        return rawOD
    
    def computeConc(self, optDensity):
        # Compute the concentration (cells/mL), based on the optical density computed.
        return 1048835.78*optDensity + 7370.76 
from machine import Pin

class Cooler:
    def __init__(self, pinPower, pinFan) -> None:
        self.power = Pin(pinPower, Pin.OUT)
        self.fan = Pin(pinFan, Pin.OUT)
    
    def fanOn(self):
        self.fan.value(1)
    
    def fanOff(self):
        self.fan.value(0)
    
    def HighPower(self):
        self.power.value(0)
    
    def LowPower(self):
        self.power.value(1)
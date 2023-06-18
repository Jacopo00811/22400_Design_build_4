from machine import Pin
import utime

class PumpStep:
    def __init__(self, pinDirection, pinStep) -> None:
        self.direction = Pin(pinDirection, Pin.OUT)
        self.step = Pin(pinStep, Pin.OUT)

    def oneStep(self):
        self.step.value(1-self.step.value())
    
    def switch_direction(self):
        self.direction.value(1-self.direction.value())
  
    def cycle(self, stepsToPerform):
        # 3200 steps equals to one full rotation
        for _ in range(stepsToPerform):
            self.oneStep()
            utime.sleep_us(10)
            self.oneStep()
            utime.sleep_us(10)

    def intermittent_step(self, sleep):
        self.oneStep()
        utime.sleep_us(sleep)
        self.oneStep()
        utime.sleep_us(sleep)
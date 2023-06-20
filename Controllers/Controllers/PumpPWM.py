from machine import Pin, PWM

class PumpPWM:
    def __init__(self, pinDirection, pinStep, speed) -> None:
        self.direction = Pin(pinDirection, Pin.OUT)
        self.step = PWM(Pin(pinStep), freq = speed, duty = 256)
    
    def switch_direction(self):
        self.direction.value(1-self.direction.value())

    def set_direction(self, direction):
        if direction not in (0, 1): # 0 - anticlockwise, 1 - clockwise
            raise ValueError("Direction must be 0 or 1")
        self.direction.value(direction)

    def set_speed(self, speed):
        self.step.freq(speed)
    
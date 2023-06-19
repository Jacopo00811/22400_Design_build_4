from machine import Pin, PWM

class LED:
    def __init__ (self)-> None:
        self.Red = PWM(Pin(17))
        self.Green = PWM(Pin(16))
        self.Blue = PWM(Pin(21))

    def turn_off_led(self):
        self.Red.duty(0)
        self.Green.duty(0)
        self.Blue.duty(0)
    
    def turn_on_led(self):
        self.Red.duty(1000)
        self.Green.duty(0)
        self.Blue.duty(1000)
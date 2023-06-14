from machine import Pin, PWM
 

"""
R -> Y
G -> B
B -> M

""" 
class LED:
    def __init__ (self)-> None:
        self.Red = PWM(Pin(17), freq = 1000)
        self.Green = PWM(Pin(16), freq = 1000)
        self.Blue = PWM(Pin(21), freq = 1000)
        self.red = 0
        self.green = 214 
        self.blue = 255

    def map_range(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

    def turn_off_led(self):
        self.Red.duty_u16(0)
        self.Green.duty_u16(0)
        self.Blue.duty_u16(0)
    
    def turn_on_led(self):
        self.Red.duty_u16(self.map_range(self.red, 0, 255, 0, 65535))
        self.Green.duty_u16(self.map_range(self.red, 0, 255, 0, 65535))
        self.Blue.duty_u16(self.map_range(self.red, 0, 255, 0, 65535))
from machine import Pin, I2C
import Resources.ssd1306

class OLED:
    def __init__(self, pinScl, pinSda):
        self.i2c = I2C(scl=Pin(pinScl), sda=Pin(pinSda), freq=400000)
        self.oled = Resources.ssd1306.SSD1306_I2C.SSD1306_I2C(128, 64, self.i2c)
        self.oled.fill(0)
        return self.oled
    
    def display_PID_controls(self, temperature, actuatorValue, parameters):
        self.oled.fill(0)
        self.oled.text('Temperature: ' + str(temperature), 0, 8)
        self.oled.text('Actuator Value: ' + str(actuatorValue), 0, 16)
        self.oled.text('PID parameters: ' + parameters, 0, 24)
       # self.oled.text() #TODO test it 
        #self.oled.text()

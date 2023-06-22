from machine import Pin, I2C
import Resources.ssd1306

class OLED:
    def __init__(self, pinScl, pinSda) -> None:
        self.i2c = I2C(scl=Pin(pinScl), sda=Pin(pinSda), freq=400000)
        self.oled = Resources.ssd1306.SSD1306_I2C(128, 32, self.i2c)
        self.oled.fill(0)
        
    
    def display_PID_controls(self, temperature, concentration, frequency, dateAndTime):
        self.oled.fill(0)
        self.oled.text('Temp: ' + str(temperature), 0, 0)
        self.oled.text('Conc.: ' + str(concentration), 0, 8)
        self.oled.text('Freq C.: ' + str(frequency), 0, 16)
        self.oled.text(str(dateAndTime), 0, 24)
        #self.oled.scroll(20, 0)
        self.oled.show()
        #self.oled.text('PID parameters: ' + parameters, 0, 24)

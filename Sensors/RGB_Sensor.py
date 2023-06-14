from machine import Pin, I2C
import Resources.tcs34725

class RGBSensor:
    def __init__(self) -> None:
        self.i2c = I2C(scl=Pin(22), sda=Pin(23), freq=400000)
        self.sensor = Resources.tcs34725.TCS34725(self.i2c)

    def set_gain(self, value):
        self.sensor.gain(value)

    def color_rgb_bytes(self, color_raw):
        """Read the RGB color detected by the sensor.  Returns a 3-tuple of
        red, green, blue component values as bytes (0-255).
        NOTE: These values are normalized against 'clear', remove the division
        by 'clear' if you need the raw values.
        """
        r, g, b, clear = color_raw
        # Avoid divide by zero errors ... if clear = 0 return black
        if clear == 0:
            return (0, 0, 0)
        red   = int(pow((int((r/clear) * 256) / 255), 2.5) * 255)
        green = int(pow((int((g/clear) * 256) / 255), 2.5) * 255)
        blue  = int(pow((int((b/clear) * 256) / 255), 2.5) * 255)
        # Handle possible 8-bit overflow
        if red > 255:
            red = 255
        if green > 255:
            green = 255
        if blue > 255:
            blue = 255
        return (red, green, blue)
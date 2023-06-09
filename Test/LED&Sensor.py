from machine import Pin, ADC, PWM, I2C
import tcs34725
from time import sleep
r = PWM(Pin(15))
g = PWM(Pin(32))
b = PWM(Pin(14))



i2c = I2C(scl=Pin(22), sda=Pin(23),freq=400000)


sensor = tcs34725.TCS34725(i2c)
sensor.gain(60)
def color_rgb_bytes(color_raw):
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

r.duty(40)
g.duty(0)
b.duty(255)

print("let there be light")
while True:
    print("RAW:  " + str(sensor.read(True)))
    # Read color sensor
    r,g,b = color_rgb_bytes(sensor.read(True))
    # Print results
    answer = '>r:{} g:{} b:{}<'.format(r, g, b)
    print(answer, end='\n')

    # Wait 1 second before repeating
    sleep(1)
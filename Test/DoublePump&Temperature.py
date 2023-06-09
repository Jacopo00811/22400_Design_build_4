from machine import Pin, PWM
from time import sleep
import Temp as tp
import utime

print("\n Mixer and Thermometer test 1.2.1")

step1 = PWM(Pin(12))
step2 = PWM(Pin(27))

direc1 = Pin(33, Pin.OUT)
direc2 = Pin(15, Pin.OUT)

direc1.value(1)
direc2.value(1)

step1.freq(5000)
step2.freq(7000)

step1.duty(1023)
step2.duty(1023)


print("\nThe thermometer alive!")

temp_sens = tp.TempSensor()

sample_last_ms = 0
SAMPLE_INTERVAL = 1000

while (True):
    if utime.ticks_diff(utime.ticks_ms(), sample_last_ms) >= SAMPLE_INTERVAL:
        temp = temp_sens.read_temp()
        #print('Thermistor temperature: ' + str(temp))
        sample_last_ms = utime.ticks_ms()

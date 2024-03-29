from machine import Pin, PWM
from time import sleep

print("\n Double mixer test 1.3.3")

step1 = PWM(Pin(12))
step2 = PWM(Pin(27))

direc1 = Pin(32, Pin.OUT)
direc2 = Pin(15, Pin.OUT)

step1.freq(8000)
step2.freq(12500)

while True:
    #direc1.value(0)
    direc2.value(0)
    direc1.value(0)

    #step1.duty(1023)
    step2.duty(1023)
    step1.duty(1023)
    
    sleep(5)
    
    direc2.value(1)
    direc1.value(1)

    sleep(5)

    step2.duty(0)
    step1.duty(0)

    sleep(2)


from machine import Pin, PWM
from time import sleep

print("\nMixer test 1")
ms1 = Pin(27, Pin.OUT)
ms2 = Pin(33, Pin.OUT)
ms3 = Pin(15, Pin.OUT)

step = PWM(Pin(14))
step.freq(1000)
step.duty(1023)

direc = Pin(12, Pin.OUT)
ms3.value(1)

i = 10000

while True:
    step.duty(1023)  # Set maximum duty cycle
    sleep(1)  # Wait for 1 second
    step.duty(0)  # Set minimum duty cycle
    sleep(1)  # Wait for 1 second
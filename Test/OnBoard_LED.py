import machine
import time

led_pin = machine.Pin(13, machine.Pin.OUT)  # Pin 13 is the onboard LED on Huzzah32

while True:
    led_pin.on()  # Turn on the LED
    time.sleep(5)  # Wait for 1 second
    led_pin.off()  # Turn off the LED
    time.sleep(1)  # Wait for 1 second

from Controllers.Cooler import Cooler
from Sensors.Temperature import TemperatureSensor
from Controllers.OLED import OLED
from Controllers.PID import PID
from Controllers.PumpPWM import PumpPWM
from Controllers.TimeAndDate import TimeAndDate
from machine import Pin
import time
import utime


def adjustSpeedCoolerPump(outputPID):
    if outputPID <= 2:
        cooler.LowPower()
        pumpCooler.set_speed(1)

    elif outputPID <= 12:
        cooler.HighPower()
        pumpCooler.set_speed(int(1000*outputPID))

    else:
        cooler.HighPower()
        pumpCooler.set_speed(10000)
        time.sleep(0.2)
        pumpCooler.set_speed(16000)
       # print(pumpCooler.step())
        # current = pumpCooler.step.freq()
        # for i in range((12500-current)//1000):
        #     time.sleep(0.05)
        #     pumpCooler.set_speed(int(current + i*1000))

temperatureSensor = TemperatureSensor(32)
oledScreen = OLED(22, 23)
pumpCooler = PumpPWM(15, 27, 1)
pumpAlgea = PumpPWM(33, 12, 1)
cooler = Cooler(4, 5)
dateAndTime = TimeAndDate(2023, 6, 13, 1, 16, 57) # TODO: ADD UPDATED PARAMETERS

# PID controller and parameters
PID = PID(temperatureSensor.read_temp(), 17)
PID.setProportional(8.5)
PID.setIntegral(3)
PID.setDerivative(0.5)

try:
    my_file = open("pid.txt") # Check if the file exists
except OSError:
    with open("pid.txt", "w") as my_file:  # If not, create it in "write" mode
        my_file.write("Test of PID \n")

# Start with high cooling power
cooler.HighPower()
cooler.fanOn()

Pinbutton = Pin(39, Pin.IN)

ACTIVATION_INTERVAL_PID = 10000 # 10s 

#Run the first activation and start timer
initalTemperature = temperatureSensor.read_temp()
initalActuatorValue = PID.update(initalTemperature)
adjustSpeedCoolerPump(initalActuatorValue)
timeActivationPump = utime.ticks_ms()

while(True):
    temperatures = []
    for i in range(10):
        temperatures.append(temperatureSensor.read_temp())
    newTemp = sum(temperatures)/10 - 1

    # PID controller
    actuatorValue = PID.update(newTemp)
    # print("\n\nActuator:" + str(actuatorValue))
    # print("Avg Temperature:" + str(newTemp))
    # print("Time:" + str(dateAndTime.date_time()))
    # print("PID Values:" + PID.overviewParameters)

    if utime.ticks_diff(utime.ticks_ms(), timeActivationPump) >= ACTIVATION_INTERVAL_PID:
        adjustSpeedCoolerPump(actuatorValue)
        timeActivationPump = utime.ticks_ms()

        print("\n\nActuator:" + str(actuatorValue))
        print("Avg Temperature:" + str(newTemp))
        print("Time:" + str(dateAndTime.date_time()))
        print("PID Values:" + PID.overviewParameters)
        print("Frequency: " + str(pumpCooler.step.freq()))
        with open("pid.txt", "a") as my_file:
            my_file.write(dateAndTime.date_time()+ ", " + str(newTemp)+ ", " + str(pumpCooler.step.freq()) + "\n")
            my_file.close()

        # Update the oled screen
        oledScreen.display_PID_controls(newTemp, actuatorValue, pumpCooler.step.freq(), dateAndTime.date_time())

    if Pinbutton.value() == 1:
        break

pumpCooler.set_speed(1)
cooler.fanOff()
print("\nSystem stopped!!!!!!")


from Controllers.Cooler import Cooler
from Controllers.PumpPWM import PumpPWM
print("\nTest n. 15")
pumpCooler = PumpPWM(15, 27, 1)
pumpCooler.set_direction(0)
pumpCooler.set_speed(1000)

cooler = Cooler(4, 5)
cooler.fanOn()
cooler.LowPower()






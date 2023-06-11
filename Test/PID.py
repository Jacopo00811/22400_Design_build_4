from Controllers.Cooler import Cooler
from Sensors.Temperature import TemperatureSensor
# from sensors.OLED import OLEDScreen
from Controllers.PID import PID
from Controllers.PumpPWM import PumpPWM
from Controllers.TimeAndDate import TimeAndDate
from machine import Pin
import time

def adjustSpeedCoolerPump(outputPID):
    if outputPID <= 2:
        cooler.LowPower()
        pumpCooler.set_speed(0)

    elif outputPID <= 20:
        cooler.LowPower()
        pumpCooler.set_speed(int(600*outputPID)) 

    else:
        cooler.HighPower()
        current = pumpCooler.step.freq()
        for i in range((12500-current)//1000):
            time.sleep(0.05)
            pumpCooler.set_speed(int(current + i*1000))

temperatureSensor = TemperatureSensor() ## TODO pin n.
# oledScreen = OLEDScreen()
pumpAlgae = PumpPWM(15, 33)  ## TODO decide if we want it and pin n.
pumpCooler = PumpPWM(27, 12) ##TODO pin n.
cooler = Cooler()
dateAndTime = TimeAndDate()

# PID controller and parameters
PID = PID(temperatureSensor.read_temp())
PID.setProportional(8.5)
PID.setIntegral(2)
PID.setDerivative(0.2)

try:
    titolo = open("pid.txt") # Check if the file exists
except OSError:
    with open("ultimo_file.txt", "w") as my_file:  # If not, create it in "write" mode
        my_file.write("First test of PID \n")

# Start with high cooling power
cooler.HighPower()
cooler.fanOn()

Pinbutton = Pin(00, Pin.IN) # TODO: Def. pin

ACTIVATION_INTERVAL_PID = 10000 # 10s 

#Run the first activation and start timer
initalTemperature = temperatureSensor.read_temp()
initalActuatorValue = PID.update(initalTemperature)
adjustSpeedCoolerPump(initalActuatorValue)
timeActivationPump = time.tick_ms()

while(True):
    temperatures = []
    for i in range(10):
        temperatures.append(temperatureSensor.read_temp())
    newTemp = sum(temperatures)/10

    with open("pid.txt", "a") as my_file:
        my_file.write(dateAndTime.date_time()+","+str(newTemp)+"\n")


    # Update the oled screen
    # oledScreen.setTemp(newTemp)
    # oledScreen.setOD
    # oledScreen.printOverview()

    # PID controller
    actuatorValue = PID.update(newTemp)
    print("Actuator:" + str(actuatorValue))
    print("Avg Temperature:" + str(newTemp))
    print("Time:" + str(dateAndTime.date_time()))
    print("PID Values:" + PID.overviewParameters)

    if time.ticks_diff(time.ticks_ms(), timeActivationPump) >= ACTIVATION_INTERVAL_PID:
        adjustSpeedCoolerPump(actuatorValue)
        timeActivationPump = time.tick_ms()

    if Pinbutton.value() == 1:
        break

pumpCooler.set_speed(0)
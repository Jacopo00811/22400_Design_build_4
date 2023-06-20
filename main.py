from Sensors.Temperature import TemperatureSensor
from Controllers.OLED import OLED
from Controllers.Cooler import Cooler
from Controllers.PID import PID
from Controllers.PumpPWM import PumpPWM
from Controllers.RGB_LED import LED
from Controllers.PumpStep import PumpStep
from Controllers.TimeAndDate import TimeAndDate
from Sensors.Light_Sensor import LightSensor
from machine import Pin, Timer
from umqtt.robust import MQTTClient
import utime
import network
import time
import utime
import os 


RUN = True

Pinbutton = Pin(39, Pin.IN)
lightSensor = LightSensor()
temperatureSensor = TemperatureSensor(32)
oledScreen = OLED(22, 23)
pumpAlgae = PumpStep(33, 12)
pumpCooler = PumpPWM(15, 27, 1)
cooler = Cooler(4, 5)
dateAndTime = TimeAndDate(2023, 6, 13, 1, 16, 57) # TODO: ADD UPDATED PARAMETERS
led = LED()
led.turn_on_led() # Turn on led


# PID controller and parameters
PID = PID(temperatureSensor.read_temp(), 17) # Terget temperature
PID.setProportional(8.5)
PID.setIntegral(3)
PID.setDerivative(0.5)

try:
    my_file = open('pid.txt') # Check if the file exists
except OSError:
    with open('pid.txt', 'w') as my_file:  # If not, create it in "write" mode
        my_file.write('Test of PID\n')

# WIFI_SSID = 'Redmi Note 11S'
# WIFI_PASSWORD = '12345678'

# random_num = int.from_bytes(os.urandom(3), 'little')
# mqtt_client_id = bytes('client_' + str(random_num), 'utf-8') # Just a random client ID

# ADAFRUIT_IO_URL = b'io.adafruit.com' 
# ADAFRUIT_USERNAME = b'Jacopo00811'
# ADAFRUIT_IO_KEY = b'aio_gAcy85Q4uB41fCKgWBfQGdvZ4Ijb'

# SYSTEMRUNNING_FEED_ID = 'system'
# TEMPERATURE_FEED_ID = 'temperature'
# OD_FEED_ID = 'od'
# PUMP1_FEED_ID = 'pump1'
# PUMP2_FEED_ID = 'pump2'
# COOLERSTATUS_FEED_ID = 'cooler'

ACTIVATION_INTERVAL_PID = 10000 # 10s 
ACTIVATION_INTERVAL_FOOD = 10000 # 10s
ACTIVATION_CONCENTRATION_MUSSEL = 10000*360*2 # 2 hrs


CLOCK_WISE_EMPTY_PUMP = 23
COUNTERCLOCK_WISE_EMPTY_PUMP = 26


mussel_number = 3
Concentration_mussel_bucket = mussel_number*1250
Concentration_mussel_bucket_at_time = 0
Volume_of_bucket = 4*1000 # mL


# sys_running_feed = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, SYSTEMRUNNING_FEED_ID), 'utf-8')
# temperature_feed = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, TEMPERATURE_FEED_ID), 'utf-8')
# OD_feed = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, OD_FEED_ID), 'utf-8') 
# pump1_feed = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, PUMP1_FEED_ID), 'utf-8') 
# pump2_feed = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, PUMP2_FEED_ID), 'utf-8')  
# cooler_status_feed = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, COOLERSTATUS_FEED_ID), 'utf-8')

def RUN_TO_FALSE():
    global RUN
    RUN = False

# def call_back(topic, msg):
#     print('Received Data:  Topic = {}, Msg = {}'.format(topic, msg))
#     recieved_data = str(msg, 'utf-8') # Recieving Data    
#     if recieved_data == "1":
#         RUN_TO_FALSE()

# def connect_wifi():
#     wifi = network.WLAN(network.STA_IF)
#     wifi.active(True)
#     wifi.disconnect()
#     wifi.connect(WIFI_SSID, WIFI_PASSWORD)
#     if not wifi.isconnected():
#         print('Connecting..')
#         timeout = 0
#         while (not wifi.isconnected() and timeout < 10):
#             print(10 - timeout)
#             timeout = timeout + 1
#             time.sleep(0.5) # TODO: MAYBE NEED MORE TIME TO CONNECT?
#     if wifi.isconnected():
#         print('Connected')
#     else:
#         wifi.disconnect()
#         print("\nNot connected... Disconnected from the server, activities will run locally\n")
#         # sys.exit()

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

# def send_data(temperature, OD, pump1, pump2, cooler):
#     try:
#         client.publish(temperature_feed, bytes(str(temperature), 'utf-8'), qos=0)
#         client.publish(OD_feed, bytes(str(OD), 'utf-8'), qos=0)
#         client.publish(pump1_feed,  bytes(str(pump1), 'utf-8'), qos=0)
#         client.publish(pump2_feed,  bytes(str(pump2), 'utf-8'), qos=0)
#         client.publish(cooler_status_feed,  bytes(str(cooler), 'utf-8'), qos=0)
#         print("Temp - ", str(temperature))
#         print("OD - ", str(OD))
#         print("Pump 1 status - ", str(pump1))
#         print("Pump 2 status - ", str(pump2))
#         print("Cooler status - ", str(cooler))
#         print('Msg sent')
#     except:
#         client.disconnect()
#         print("\nDisconnected from the server, activities will run locally\n")
#         # sys.exit()

def read_temperature(temperatureSensor):
    temperatures = [] 
    i = 10 # Samples to average on (Note: read_temp() already averages over 50 readings)
    for _ in range(i):
        temperatures.append(temperatureSensor.read_temp())
    newTemp = sum(temperatures)/i - 1 # Temperature sensor off-set compensation
    return newTemp

# connect_wifi() # Connecting to WiFi Router 

# client = MQTTClient(client_id = mqtt_client_id, 
#                     server = ADAFRUIT_IO_URL, 
#                     user = ADAFRUIT_USERNAME, 
#                     password = ADAFRUIT_IO_KEY,
#                     ssl = False)

# try:            
#     client.connect()
# except Exception as e:
#     print('Could not connect to MQTT server {}{}'.format(type(e).__name__, e))
#     client.disconnect()
#     print("\nDisconnected from the server, activities will run locally\n")
#     # sys.exit()
        
# # Define call back function
# client.set_callback(call_back) # Callback function               
# client.subscribe(sys_running_feed) # Subscribing to particular topic


"""
This allows to send date with an independet timer

timer = Timer(0)
timer.init(period = 10000, mode = Timer.PERIODIC, 
           callback = send_data(read_temperature(temperatureSensor), read_OD(lightSensor),
                                 True if pumpCooler.step.freq() else False,                       
                                 True if pumpAlgea.step.freq() else False, "12 V" if cooler.power.value() == 0 else "5 V"))

"""

#Run the first activation and start timer
initalTemperature = temperatureSensor.read_temp()
initalActuatorValue = PID.update(initalTemperature)
adjustSpeedCoolerPump(initalActuatorValue)
timeActivationPump = utime.ticks_ms()

#Run the first feed and start timer
mLOfFood = -Volume_of_bucket*(Concentration_mussel_bucket_at_time - Concentration_mussel_bucket)/(lightSensor.computeConc(lightSensor.computeOD()) - Concentration_mussel_bucket)
cycles_clockwise = mLOfFood/0.3155 + CLOCK_WISE_EMPTY_PUMP # Feed the mussel
cycles_couterclockwise =  mLOfFood/0.2868 + COUNTERCLOCK_WISE_EMPTY_PUMP # Feed the algae
pumpAlgae.direction_clockwise()
pumpAlgae.cycle(cycles_clockwise)
timeActivationFood = utime.ticks_ms()

while RUN == True:
    newTemp = read_temperature(temperatureSensor)

    # PID controller
    actuatorValue = PID.update(newTemp)

    # Check messages from subscribed feeds
    # try:
    #     client.check_msg()
    # except:
    #     client.disconnect()
    #     print("\nDisconnected from the server, activities will run locally\n")
    #     # sys.exit()

    if utime.ticks_diff(utime.ticks_ms(), timeActivationPump) >= ACTIVATION_INTERVAL_PID:
        adjustSpeedCoolerPump(actuatorValue)
        timeActivationPump = utime.ticks_ms()
        # print("\n\nActuator:" + str(actuatorValue))
        # print("Avg Temperature:" + str(newTemp))
        # print("Time:" + str(dateAndTime.date_time()))
        # print("PID Values:" + PID.overviewParameters)
        # print("Frequency cooler pump: " + str(pumpCooler.step.freq()))

        pump1 = pumpCooler.step.freq()
        pump2 = pumpAlgae.step.freq()
        ODValue = lightSensor.computeOD()
        concentration = lightSensor.computeConc(ODValue)
        
        # Write to file
        with open("pid.txt", "a") as my_file:
            my_file.write(dateAndTime.date_time()+ ", " + str(newTemp)+ ", " + str(pumpCooler.step.freq()) + ", " + str(concentration) + "\n")
            my_file.close()

        # Send to the cloud
        # TODO: Might want to add an if statement to check if there's connection to avoid 
        #send_data(newTemp, ODValue, pump1, pump2, "12 V" if cooler.power.value() == 0 else "5 V")

        # Update the oled screen
        oledScreen.display_PID_controls(newTemp, concentration, pump1, dateAndTime.date_time()) # TODO: Display number of cells or OD instead of date and time

    if (utime.ticks_diff(utime.ticks_ms(), timeActivationFood) >= ACTIVATION_INTERVAL_FOOD):
        pumpAlgae.direction_counterclockwise()
        pumpAlgae.cycle(cycles_couterclockwise)
        
        Concentration_mussel_bucket_at_time = 750

        mLOfFood = -Volume_of_bucket*(Concentration_mussel_bucket_at_time - Concentration_mussel_bucket)/(lightSensor.computeConc(lightSensor.computeOD()) - Concentration_mussel_bucket)
        cycles_clockwise = mLOfFood/0.3155 + CLOCK_WISE_EMPTY_PUMP # Feed the mussel
        cycles_couterclockwise =  mLOfFood/0.2868 + COUNTERCLOCK_WISE_EMPTY_PUMP # Feed the algae
        
        pumpAlgae.direction_clockwise()
        pumpAlgae.cycle(cycles_clockwise)

        timeActivationFood = utime.ticks_ms()

    if Pinbutton.value() == 1:
        RUN_TO_FALSE()
        break

# Turn off system
pumpCooler.set_speed(1)
cooler.fanOff()
print("\n-------------------------------------------------\n")
print("------------------System stopped!!!!!!---------------")
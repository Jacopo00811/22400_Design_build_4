from machine import Pin, Timer
import network
import time
from umqtt.robust import MQTTClient
import sys
import os 

WIFI_SSID = 'Redmi Note 11S'
WIFI_PASSWORD = '12345678'

random_num = int.from_bytes(os.urandom(3), 'little')
mqtt_client_id = bytes('client_'+str(random_num), 'utf-8') # Just a random client ID

ADAFRUIT_IO_URL = b'io.adafruit.com' 
ADAFRUIT_USERNAME = b'Jacopo00811'
ADAFRUIT_IO_KEY = b'aio_gAcy85Q4uB41fCKgWBfQGdvZ4Ijb'

SYSTEMRUNNING_FEED_ID = 'system'
TEMPERATURE_FEED_ID = 'temperature'
OD_FEED_ID = 'od'
PUMP1_FEED_ID = 'pump1'
PUMP2_FEED_ID = 'pump2'
COOLERSTATUS_FEED_ID = 'cooler'

def cb(topic, msg):                             # Callback function
    print('Received Data:  Topic = {}, Msg = {}'.format(topic, msg))
    recieved_data = str(msg,'utf-8')            #   Recieving Data    
    if recieved_data=="1":
        # Turn off system
        exit

def connect_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.disconnect()
    wifi.connect(WIFI_SSID, WIFI_PASSWORD)
    if not wifi.isconnected():
        print('Connecting..')
        timeout = 0
        while (not wifi.isconnected() and timeout < 10):
            print(10 - timeout)
            timeout = timeout + 1
            time.sleep(0.5) ### MAYBE NEED MORE TIME
    if wifi.isconnected():
        print('Connected')
    else:
        print('Not connected')
        sys.exit()
        
def sens_data(data):
    exit
    # sensor.measure()                    # Measuring 
    # temp = sensor.temperature()         # getting Temp
    # hum = sensor.humidity()
    # client.publish(temp_feed,    
    #               bytes(str(temp), 'utf-8'),   # Publishing Temprature to adafruit.io
    #               qos=0)
    
    # client.publish(hum_feed,    
    #               bytes(str(hum), 'utf-8'),   # Publishing Temprature to adafruit.io
    #               qos=0)
    # print("Temp - ", str(temp))
    # print("Hum - " , str(hum))
    # print('Msg sent')

connect_wifi() # Connecting to WiFi Router 

client = MQTTClient(client_id = mqtt_client_id, 
                    server = ADAFRUIT_IO_URL, 
                    user = ADAFRUIT_USERNAME, 
                    password = ADAFRUIT_IO_KEY,
                    ssl = False)

try:            
    client.connect()
except Exception as e:
    print('Could not connect to MQTT server {}{}'.format(type(e).__name__, e))
    sys.exit()
        
sys_running_feed = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, SYSTEMRUNNING_FEED_ID), 'utf-8')
temperature_feed = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, TEMPERATURE_FEED_ID), 'utf-8')
OD_feed = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, OD_FEED_ID), 'utf-8') 
pump1_feed = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, PUMP1_FEED_ID), 'utf-8') 
pump2_feed = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, PUMP2_FEED_ID), 'utf-8')  
cooler_status_feed = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, COOLERSTATUS_FEED_ID), 'utf-8')

client.set_callback(cb)      # Callback function               
client.subscribe(sys_running_feed) # Subscribing to particular topic

timer = Timer(0)
timer.init(period = 5000, mode = Timer.PERIODIC, callback = sens_data)

# For subscribed feeds
while True:
    try:
        client.check_msg()                  # non blocking function
    except :
        client.disconnect()
        sys.exit()


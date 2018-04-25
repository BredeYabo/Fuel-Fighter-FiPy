#Developed to test the MQTT (#1) and 4G capabilities (#2) #execfile("/flash/mqttFF.py")

from network import WLAN
from mqtt import MQTTClient
import machine
import time

def sub_cb(topic, msg):
   print(msg)

wlan = WLAN(mode=WLAN.STA)
wlan.connect("Android", auth=(WLAN.WPA2, "123456789a"), timeout=5000)

while not wlan.isconnected():
    machine.idle()
print("Connected to Wifi\n")

client = MQTTClient("FiPy", "129.241.91.125",user="username", password="ff", port=1883)

client.set_callback(sub_cb)
client.connect()
client.subscribe(topic="Fuelfighter")

print("Sending ON")
client.publish(topic="Fuelfighter", msg="123,2,1,0,1,0,1,0,1,256,42000")
time.sleep(1)

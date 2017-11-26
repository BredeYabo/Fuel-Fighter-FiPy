#Program to only send GPS coordinates
from pytrack import Pytrack
from L76GNSS import L76GNSS
from LIS2HH12 import LIS2HH12
from startiot import Startiot
from network import LoRa
import pycom
import time
import socket
iot = Startiot()
pycom.heartbeat(False)

#from pytrack import Pytrack
#from L76GNSS import L76GNSS
#l76 = L76GNSS(py, timeout=25)
#print(l76.coordinates(True))


py = Pytrack()
gps = L76GNSS(py)
acc = LIS2HH12(py)
print("\nNow running sendGPS.py\n")
print("\nNow attempting to establish LoPy connection\n")
pycom.rgbled(0xFF0000)
iot.connect()#Line to estalish connection
pycom.rgbled(0x0000FF)
print("\nConnection now established\n")

default_attempts=20
while default_attempts!=0:
    m_lat, m_lng = gps.coords()
    print('Coords:', "{},{}".format(m_lat, m_lon))
    acc.read()
    m_roll = acc.roll()
    m_pitch = acc.pitch()
    m_yaw = acc.yaw()
    print('Roll:', m_roll)
    print('Pitch:', m_pitch)
    print('Yaw:', m_yaw)
    data = "{},{},{},{},{}".format(m_lat, m_lng, m_roll, m_pitch, m_yaw)
    print(data)
    print("\nSend data...",  default_attempts)
    data=str(str(data)+"\nAttempt number: "+str(20-default_attempts))
    print(data)
    default_attempts-=1
    iot.send(data)
    pycom.rgbled(0x00ff00)
    time.sleep(0.1)
    pycom.rgbled(0x000000)
    time.sleep(0.1)
    pycom.rgbled(0x00ff00)
    time.sleep(0.1)
    pycom.rgbled(0x000000)
    print("Sending data done...")
    data = iot.recv(64)
    print("Received Data:",  data)
    time.sleep(2)

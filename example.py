from pytrack import Pytrack
from L76GNSS import L76GNSS
from LIS2HH12 import LIS2HH12

from startiot import Startiot

from network import LoRa

import time
import pycom
import socket

py = Pytrack()
gps = L76GNSS(py)
acc = LIS2HH12(py)

pycom.heartbeat(False) # disable the blue blinking
pycom.rgbled(0x000000) #LED off

iot = Startiot()
iot.connect(False)

# main loop
while True:
 print('----------------------------------')

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
 count = count + 1

 iot.send(data)

 time.sleep(30)

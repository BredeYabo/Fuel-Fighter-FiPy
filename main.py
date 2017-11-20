# main.py -- put your code here!
#Edited by Sebastian
#"execfile('/flash/file.py')" To run "file.py"m
#execfile('/flash/CTA.py')#Temp Disabled, but works (it connects to my android WiFi hotspot)
#execfile('/flash/RGBPARTY.py')
from startiot import Startiot
import pycom
import time
pycom.heartbeat(False) # disable the blue blinking
iot = Startiot()

pycom.rgbled(0xFF0000)
iot.connect()
pycom.rgbled(0x0000FF)

count = 0
while True:
  print("Send data...",  count)
  data = "Fuel Fighter Signal Test: %s" % (count)
  count = count + 1

  # send some data
  iot.send(data)
  pycom.rgbled(0x00ff00)
  time.sleep(0.1)
  pycom.rgbled(0x000000)
  time.sleep(0.1)
  pycom.rgbled(0x00ff00)
  time.sleep(0.1)
  pycom.rgbled(0x000000)
  print("Sending data done...")

  # get any data received
  data = iot.recv(64)
  print("Received Data:",  data)

  time.sleep(5)

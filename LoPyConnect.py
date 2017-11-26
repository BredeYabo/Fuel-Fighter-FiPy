#Edited by Sebastian Kleivenes, original file from Telenor
from startiot import Startiot
import pycom
import time
pycom.heartbeat(False) # disable the blue blinking
iot = Startiot()

#Data to Send
attempts=0
def what_data():
    ask=input("\nWhat message would you like to send?\n")
    attempts=input("\nHow many times would you like me to try and send the signal?\nEach signal takes 2s, hence 10 attempts = 20seconds\n")
    a=[ask, attempts]
    return a
a=what_data()
ask=a[0]
attempts=int(a[1])
print("\nNow attempting to establish LoPy connection\n")
pycom.rgbled(0xFF0000)
iot.connect()#Line to estalish connection
pycom.rgbled(0x0000FF)
print("\nConnection now established\n")
#count = 0
#datacount = 0
init_at=attempts
while attempts!=0:
    print("\nSend data..."+str(init_at-attempts))
    data=str(ask+"   attempt number :"+str(init_at-attempts))
    print(data)
#  data = "Fuel Fighter Signal Test: %s" % (datacount)
#  count = count + 1
#  if count%10==0:
#      datacount+=1
# send some data
    attempts-=1
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
    time.sleep(2)
#    if datacount==11:
#        break

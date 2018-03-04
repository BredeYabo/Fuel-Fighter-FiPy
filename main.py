#by Sebastian Kleivenes
from machine import SD
from pycom import heartbeat as hb
from os import listdir as ls
from os import mount as m
import os
hb(False)
sd = SD()
m(sd, '/sd')
print("Pycom up and running!")
#print("\n"*3+"Hi, we are up and running!\n")
#choice=input("What would you like to do?"+"\n"*3+"1. Send a custom message over LoPy\n2. Send GPS coordinates over LoPy\n3. Test for GPS coordinates\n4. Connect to Phone hotspot (Defualt Sebastian's Phone's Hotspot)\n5. Connect to any WiFi using WPA2\n6. Test the RGB Lights\n7. Test the Accelerometer\n8. Run UART_ULTIMATE\n9. Test the SD CARD"+"\n"*2+"(type 1/2/3 etc)"+"\n"*2+"- ")
choice=99
if choice=="1":
    execfile('/flash/LoPyConnect.py')
if choice=="2":
    execfile('/flash/sendGPS.py')
if choice=="3":
    execfile('/flash/GPSTest.py')
if choice=="4":
    execfile('/flash/CTA.py')
if choice=="5":
    execfile('/flash/ConnectWIFI.py')
if choice=="6":
    execfile('/flash/RGBPARTY.py')
if choice=="7":
    execfile('/flash/pytrack_acc.py')
if choice=="8":
    execfile('/flash/UART_ULTIMATE.py')
if choice=="9":
    execfile('/flash/SD_CARD.py')
if choice==9:
    execfile('/flash/TEST_DAY_1.py')

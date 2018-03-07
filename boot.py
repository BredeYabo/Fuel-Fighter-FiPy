# boot.py -- run on boot-up
import os
from machine import UART
from machine import SD
from os import mount as m
from os import listdir as ls
from pycom import heartbeat as hb
from pycom import rgbled as LED
from time import sleep as ts
from utime import ticks_ms as ut
import os
uart = UART(0, 115200)
os.dupterm(uart)
try:
    sd = SD()
    m(sd, '/sd')
except:
    print("ERROR: Failed to mount SD - Card!")
hb(False)
LED_green=0x007f00
LED_red=0x7f0000
LED_yellow=0x7f7f00

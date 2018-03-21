# boot.py -- run on boot-up
import os
from machine import UART
from machine import SD
from os import mount as m
from os import listdir as ls
from os import mkdir
from os import remove
from pycom import heartbeat as hb
from pycom import rgbled as LED
from time import sleep as ts
from utime import ticks_ms as ut
from utime import ticks_cpu as cputime
import os
uart = UART(0, 115200)
os.dupterm(uart)
try:
    sd = SD()
    m(sd, '/sd')
except:
    print("\nERROR: Failed to mount SD - Card!")
hb(False)
LED_red=0xFF0000
LED_red_soft=0x110000
LED_green=0x00FF00
LED_green_soft=0x001100
LED_blue=0x0000FF
LED_blue_soft=0x000011
LED_yellow=0xFFFF00
LED_yellow_soft=0x111100
LED_pink=0xFF00AA
LED_pink_soft=0x200011
LED_off=0x000000

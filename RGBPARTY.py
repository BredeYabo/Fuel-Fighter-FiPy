#Testing Auto Run on-boot Files by Sebastian Kleivenes
import pycom
import time
p=pycom
p.heartbeat(False)
green=0x007f00
red=0x7f0000
yellow=0x7f7f00
t=time
b=0
LED=p.rgbled
while b<5:
    b+=1
    LED(red)
    t.sleep(1)
    LED(green)
    t.sleep(1)
    LED(yellow)
    t.sleep(1)
p.heartbeat(True)

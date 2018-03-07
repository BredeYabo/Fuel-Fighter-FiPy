#Testing Auto Run on-boot Files by Sebastian Kleivenes
import time

t=time
b=0
hb(False)
while b<5:
    b+=1
    LED(red)
    t.sleep(1)
    LED(green)
    t.sleep(1)
    LED(yellow)
    t.sleep(1)

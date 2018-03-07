from LIS2HH12 import LIS2HH12
from pytrack import Pytrack
py = Pytrack()
acc = LIS2HH12()
n=0
while True:
   pitch = acc.pitch()
   roll = acc.roll()
   print('{},{}'.format(pitch,roll))
   ts(1)
   n+=1
   if n==50:
       break

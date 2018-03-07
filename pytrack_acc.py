from LIS2HH12 import LIS2HH12
from pytrack import Pytrack
py = Pytrack()
acc = LIS2HH12()
n=0
while True:
   print('{},{}'.format(acc.pitch(),acc.roll()))
   ts(1)
   n+=1
   if n==50:
       break

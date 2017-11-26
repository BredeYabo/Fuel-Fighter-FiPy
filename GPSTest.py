from pytrack import Pytrack
from L76GNSS import L76GNSS
py = Pytrack()
gps = L76GNSS(py)
c=0
a=int(input("\nHow many times do you want to test the GPS coordinates?\n"))
t=int(input("What would you like the timeout to be for the GPS?\n"))
while True:
    l76 = L76GNSS(py, timeout=t)
    print(l76.coordinates(True))
    c+=1
    if c==a:
        break

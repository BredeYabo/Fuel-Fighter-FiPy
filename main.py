#by Sebastian Kleivenes
print("\n"*3+"Hi, we are up and running!\n")
print("Current status: LoPy unstable; GPS not working")
choice=input("What would you like to do?"+"\n"*3+"1. Send a custom message over LoPy\n2. Send GPS coordinates over LoPy\n3. Test for GPS coordinates\n4. Connect to Phone hotspot (Defualt Sebastian's Phone's Hotspot)\n5. Connect to any WiFi using WPA2\n6. Test the RGB Lights"+"\n"*2+"(type 1/2/3 etc)"+"\n"*2+"- ")
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

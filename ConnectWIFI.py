#To connect to WiFi, - Sebastian Kleivenes
from network import WLAN #Imports
wlan=WLAN(mode=WLAN.STA)
SSID=input("\nThis is for connecting to WiFi using WPA2 authentication\nWhat's the SSID of the network you are trying to connect to? ")
WP=input("What's the password? ")
wlan.connect(SSID, auth=(WLAN.WPA2,WP), timeout=5000)
WLAN().ifconfig() #Provides local IP

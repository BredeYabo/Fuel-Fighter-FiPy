#To connect to WiFi, - Sebastian Kleivene (*File Not tested)
from network import WLAN #Imports
wlan=WLAN(mode=WLAN.STA)
wlan.connect('SSID OF NETWORK', auth=(WLAN.WPA2,'PASSWORD'), timeout=5000)
WLAN().ifconfig() #Provides local IP

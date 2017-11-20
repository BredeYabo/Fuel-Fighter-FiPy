#CTA=Connect to Android By Sebastian Kleivenes
# if SSID="Android" & Password "boyswillbeboys"
from network import WLAN #Imports
wlan=WLAN(mode=WLAN.STA)
wlan.connect('Android', auth=(WLAN.WPA2,'boyswillbeboys'), timeout=5000)
WLAN().ifconfig() #Provides local IP

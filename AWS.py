from MQTTLib import AWSIoTMQTTClient
from network import WLAN
import time
import AWSconfig
LED(LED_green_soft)
# Connect to wifi
wlan = WLAN(mode=WLAN.STA)
wlan.connect(AWSconfig.WIFI_SSID, auth=(None, AWSconfig.WIFI_PASS), timeout=5000)
while not wlan.isconnected():
    time.sleep(0.5)
print('WLAN connection succeeded!')
#execfile('/flash/AWS.py')

# user specified callback function
def customCallback(client, userdata, message):
	print("Received a new message: ")
	print(message.payload)
	print("from topic: ")
	print(message.topic)
	print("--------------\n\n")

# configure the MQTT client
pycomAwsMQTTClient = AWSIoTMQTTClient(AWSconfig.CLIENT_ID, password='ff', user='username')
pycomAwsMQTTClient.configureEndpoint(AWSconfig.AWS_HOST, AWSconfig.AWS_PORT)
pycomAwsMQTTClient.configureOfflinePublishQueueing(AWSconfig.OFFLINE_QUEUE_SIZE)
pycomAwsMQTTClient.configureDrainingFrequency(AWSconfig.DRAINING_FREQ)
pycomAwsMQTTClient.configureConnectDisconnectTimeout(AWSconfig.CONN_DISCONN_TIMEOUT)
pycomAwsMQTTClient.configureMQTTOperationTimeout(AWSconfig.MQTT_OPER_TIMEOUT)
pycomAwsMQTTClient.configureLastWill(AWSconfig.LAST_WILL_TOPIC, AWSconfig.LAST_WILL_MSG, 1)

#Connect to MQTT Host
if pycomAwsMQTTClient.connect():
    print('connection succeeded')

# Subscribe to topic
#pycomAwsMQTTClient.subscribe(AWSconfig.TOPIC, 1, customCallback)
#time.sleep(2)

# Send message to host
loopCount = 0
fileAWS=open('/sd/update.txt','r')
#line='123,2,1,0,1,0,1,0,1,256,42000'
while loopCount < 10:
    fileAWS=open('/sd/update.txt','r')
    pycomAwsMQTTClient.publish(AWSconfig.TOPIC,fileAWS.read(), 1)
    fileAWS.close()
    loopCount += 1
    ts(1)

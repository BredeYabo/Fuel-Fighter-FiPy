#CTA=Connect to Android By Sebastian Kleivenes
# if SSID="Android" & Password "password"
import time
from network import WLAN #Imports
wlan=WLAN(mode=WLAN.STA)
wlan.connect('Android', auth=(WLAN.WPA2,'123456789a'), timeout=5000)
WLAN().ifconfig() #Provides local IP

AWS_PORT = 8883
AWS_HOST = 'a2tm8m18pdjk7u.iot.us-west-2.amazonaws.com'
AWS_ROOT_CA = '/flash/cert/aws_root.ca'
AWS_CLIENT_CERT = '/flash/cert/FiPy-FF.cert.pem'
AWS_PRIVATE_KEY = '/flash/cert/721d04c76e-public.pem.key'
# user specified callback function
def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")
CLIENT_ID = 'PycomPublishClient'
TOPIC = 'PublishTopic'
OFFLINE_QUEUE_SIZE = -1
DRAINING_FREQ = 2
CONN_DISCONN_TIMEOUT = 10
MQTT_OPER_TIMEOUT = 5
LAST_WILL_TOPIC = 'PublishTopic'
LAST_WILL_MSG = 'To All: Last will message'
# configure the MQTT client
pycomAwsMQTTClient = AWSIoTMQTTClient(CLIENT_ID)
pycomAwsMQTTClient.configureEndpoint(AWS_HOST, AWS_PORT)
pycomAwsMQTTClient.configureCredentials(AWS_ROOT_CA, AWS_PRIVATE_KEY, AWS_CLIENT_CERT)

pycomAwsMQTTClient.configureOfflinePublishQueueing(OFFLINE_QUEUE_SIZE)
pycomAwsMQTTClient.configureDrainingFrequency(DRAINING_FREQ)
pycomAwsMQTTClient.configureConnectDisconnectTimeout(CONN_DISCONN_TIMEOUT)
pycomAwsMQTTClient.configureMQTTOperationTimeout(MQTT_OPER_TIMEOUT)
pycomAwsMQTTClient.configureLastWill(LAST_WILL_TOPIC, LAST_WILL_MSG, 1)

#Connect to MQTT Host
if pycomAwsMQTTClient.connect():
    print('AWS connection succeeded')

# Subscribe to topic
pycomAwsMQTTClient.subscribe(TOPIC, 1, customCallback)
time.sleep(2)

# Send message to host
loopCount = 0
while loopCount < 8:
    pycomAwsMQTTClient.publish(TOPIC, "New Message " + str(loopCount), 1)
    loopCount += 1
    time.sleep(5.0)

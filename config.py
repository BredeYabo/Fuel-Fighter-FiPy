
# wifi configuration
WIFI_SSID = 'Android'
WIFI_PASS = '123456789a'

# AWS general configuration
AWS_PORT = 8883
AWS_HOST = 'a2tm8m18pdjk7u.iot.us-west-2.amazonaws.com'
AWS_ROOT_CA = '/flash/cert/aws-root.ca'
AWS_CLIENT_CERT = '/sd/cert/94f10db729-certificate.pem.crt'
AWS_PRIVATE_KEY = '/sd/cert/94f10db729-private.pem.key'

################## Subscribe / Publish client #################
CLIENT_ID = 'PycomPublishClient'
TOPIC = 'PublishTopic'
OFFLINE_QUEUE_SIZE = -1
DRAINING_FREQ = 2
CONN_DISCONN_TIMEOUT = 10
MQTT_OPER_TIMEOUT = 5
LAST_WILL_TOPIC = 'PublishTopic'
LAST_WILL_MSG = 'To All: Last will message'

####################### Shadow updater ########################
#THING_NAME = "my thing name"
#CLIENT_ID = "ShadowUpdater"
#CONN_DISCONN_TIMEOUT = 10
#MQTT_OPER_TIMEOUT = 5

####################### Delta Listener ########################
#THING_NAME = "my thing name"
#CLIENT_ID = "DeltaListener"
#CONN_DISCONN_TIMEOUT = 10
#MQTT_OPER_TIMEOUT = 5

####################### Shadow Echo ########################
#THING_NAME = "my thing name"
#CLIENT_ID = "ShadowEcho"
#CONN_DISCONN_TIMEOUT = 10
#MQTT_OPER_TIMEOUT = 5

import time
import paho.mqtt.client as paho
from paho import mqtt
from paho.mqtt.client import CallbackAPIVersion
from random import uniform


def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)


def on_publish(client, userdata, mid, reason_code, properties=None):
    print(f"Published message id: {mid}, Reason Code: {reason_code}")


def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


client = paho.Client(callback_api_version=CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish

client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.username_pw_set("user1", "User1234")
client.connect("d2f277161aef4f56a41ef426746a4219.s1.eu.hivemq.cloud", 8883)

client.loop_start()

# Publish every 2 seconds
while True:
    randNumber = round(uniform(20.0, 21.0), 2)
    client.publish("iot/device/control", payload="OFF", qos=1)
    time.sleep(2)

import time
import paho.mqtt.client as paho
from paho import mqtt
from util.Config import *
from datas.serializers import DataSerializer
import json


class Client:
    # setting callbacks for different events to see if it works, print the message etc.
    def on_connect(self, client, userdata, flags, rc, properties=None):
        print("CONNACK received with code %s." % rc)

    # with this callback you can see if your publish was successful
    def on_publish(self, client, userdata, mid, properties=None):
        print("mid: " + str(mid))

    # print which topic was subscribed to
    def on_subscribe(self, client, userdata, mid, granted_qos, properties=None):
        print("Subscribed: " + str(mid) + " " + str(granted_qos))

    # print message, useful for checking if it was successful
    def on_message(self, client, userdata, msg):
        if msg.payload != "":
            self.container.append(convert(str(msg.payload, "utf-8")))
            print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

    def __init__(self):
        # using MQTT version 5 here, for 3.1.1: MQTTv311, 3.1: MQTTv31
        # userdata is user defined data of any type, updated by user_data_set()
        # client_id is the given name of the client
        self.container = []
        self.client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
        self.client.on_connect = self.on_connect

        # enable TLS for secure connection
        self.client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        # set username and password
        self.client.username_pw_set(USERNAME_CLOUD, PASSWORD_CLOUD)
        # connect to HiveMQ Cloud on port 8883 (default for MQTT)
        self.client.connect(DOMAIN_CLOUD, PORT_CLOUD)

        # setting callbacks, use separate functions like above for better visibility
        self.client.on_subscribe = self.on_subscribe
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish

        # subscribe to all topics of encyclopedia by using the wildcard "#"
        self.client.subscribe(TOPIC, qos=1)

        # loop_forever for simplicity, here you need to stop the loop manually
        # you can also use loop_start and loop_stop
        self.client.loop_start()
        time.sleep(1000)
        if len(self.container) != 0:
            if len(self.container[0]) != 0:
                self.client.publish("YourTopic/A/B/C", payload="", qos=1, retain=True)
        self.client.loop_stop()

    def get_messages(self):
        return self.container


def convert(s):
    if s != "":
        return json.loads(s)
    return ""

class PublicClient:
    def on_publish(self, client, userdata, mid, properties=None):
        print("mid: " + str(mid))

    def on_subscribe(self, client, userdata, mid, granted_qos):
        print("Subscribed: " + str(mid) + " " + str(granted_qos))

    def on_message(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload, "utf-8"))
        try:
            DataSerializer.create_new_data(convert(str(msg.payload, "utf-8")))
        except:
            pass

    def __init__(self):
        self.client = paho.Client()
        self.client.on_subscribe = self.on_subscribe
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish
        self.client.connect(DOMAIN_CLOUD, PORT_CLOUD)
        self.client.subscribe(TOPIC, qos=1)

    def loop(self):
        self.client.loop_forever()

    def send_command(self, command, api_key, device, speed=None):
        data = dict()
        data["command"] = command
        data["device"] = device
        data["api_key"] = api_key
        if speed != None:
            data["speed"] = speed
        self.client.publish(TOPIC, json.dumps(data))

if __name__ == '__main__':
    client = PublicClient()
    client.send_command("ON", "7bf59e593a524c16bbdca0465c4b19194ad797c5", 5)

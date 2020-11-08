"""
Client MQTT
"""

import paho.mqtt.client as mqtt
import threading
import time
import re
from .config import get_config


REQUEST_PREFIX = "$share/caffael/dispatch/"
REPLY_PREFIX = "$share/caffael/reply/"


def _queue_thread(client):
    client.loop_forever()

def sanitize_topic(topic):
    return re.sub("[^0-9a-zA-Z]+", "_", topic).lower().rstrip("_").lstrip("_")


class MQTT(object):

    def __init__(self, queue_name, handler):
        self.config = get_config().get('mqtt')
        topic = sanitize_topic(queue_name)
        self.request_topic = REQUEST_PREFIX + topic
        self.reply_topic = REPLY_PREFIX + topic
        self.handler = handler

    def on_connect(self, client, userdata, flags, rc):
        client.subscribe(self.request_topic)

    def on_message(self, client, userdata, msg):
        response = self.handler(msg.payload)
        self.reply(response)

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            print ("Unexpected MQTT disconnection. Will auto-reconnect")

    def connect(self):
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.on_disconnect = self.on_disconnect

        config = get_config()['mqtt']
        if config.get('username') and config.get('password'):
            client.username_pw_set(username=config.get('username'), password=config.get('password'))
        client.connect(config.get('broker'), int(config.get('port')), 60)

        queue_thread = threading.Thread(target=_queue_thread, args=(client,))
        queue_thread.daemon = True
        queue_thread.start()
        self.client = client

    def reply(self, message):
        self.client.publish(self.reply_topic, payload=message, qos=2, retain=False)
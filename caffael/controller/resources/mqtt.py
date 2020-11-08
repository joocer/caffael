"""
MQTT

Creates 
"""

import paho.mqtt.client as mqtt
import threading
import time
import re
from .config import get_config

_queues = {}

DISPATCH_PREFIX = "caffael/dispatch/"
REPLY_PREFIX = "caffael/reply/"

def initialize_bus():
    global get_bus
    _mq = MQTT()
    _mq.connect()
    get_bus = lambda: _mq
    return _mq

get_bus = initialize_bus

def on_connect(client, userdata, flags, rc):
    client.subscribe(REPLY_PREFIX + '#')

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print ("Unexpected MQTT disconnection. Will auto-reconnect")

def on_message(client, userdata, msg):
    topic = msg.topic.lstrip(REPLY_PREFIX)
    topic = REPLY_PREFIX + sanitize_topic(topic)
    handler = _queues.get(topic, deadletter)
    handler(topic, msg)

def deadletter(topic, userdata):
    raise Exception(f'Unhandled Message Topic: {topic}')

def _queue_thread(client):
    client.loop_forever()

def sanitize_topic(topic):
    return re.sub("[^0-9a-zA-Z]+", "_", topic).lower().rstrip("_").lstrip("_")


class MQTT(object):

    def __init__(self):
        self.config = get_config().get('mqtt')

    def connect(self):
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
        client.on_disconnect = on_disconnect

        config = get_config()['mqtt']
        if config.get('username') and config.get('password'):
            client.username_pw_set(username=config.get('username'), password=config.get('password'))
        client.connect(config.get('broker'), int(config.get('port')), 60)

        queue_thread = threading.Thread(target=_queue_thread, args=(client,))
        queue_thread.daemon = True
        queue_thread.start()
        self.client = client

    def add_listener(self, queue_name, callback):
        topic = REPLY_PREFIX + sanitize_topic(queue_name)
        _queues[topic] = callback

    def dispatch(self, queue_name, message):
        topic = DISPATCH_PREFIX + sanitize_topic(queue_name)
        print("dispatching to", topic)
        self.client.publish(topic, payload=message, qos=2, retain=False)
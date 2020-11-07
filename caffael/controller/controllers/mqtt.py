"""
MQTT

Creates 
"""

#from .base_queue import BaseQueue
import paho.mqtt.client as mqtt
import threading
import queue
import time

_queues = {}

DISPATCH_PREFIX = "$share/caffael/dispatch"
REPLY_PREFIX = "$share/caffael/reply"


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe('caffael/reply/#')

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print ("Unexpected MQTT disconnection. Will auto-reconnect")

def on_message(client, userdata, msg):
    print(msg.topic)
    queue = get_queue(msg.topics)
    queue.put_nowait()

def _queue_thread(client, config):

    if config.get('username') and config.get('password'):
        client.username_pw_set(username=config.get('username'), password=config.get('password'))
    client.connect_async(config.get('broker'), config.get('port'), 60)
    while True:
        client.loop()
        for q in _queues:
            if not q.empty():
                item = q.get_nowait()
                client.publish(q, item)
        time.sleep(0.1)

def get_queue(topic):
    """
    Call this to get an instance of the queue list
    """
    if topic not in _queues:
        new_queue = queue.SimpleQueue()
        _queues[topic] = new_queue
        print(f"Created new queue: {topic}")
    return _queues.get(topic)


class MQTT(object):

    def __init__(self, config):
        self.config = config

    def connect(self):
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
        client.on_disconnect = on_disconnect

        queue_thread = threading.Thread(target=_queue_thread, args=(client,self.config))
        queue_thread.daemon = True
        queue_thread.start()
        
        self.client = client
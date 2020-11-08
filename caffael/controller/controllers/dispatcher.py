"""
Dispatcher
"""

import uuid
import datetime
from ..resources import get_bus

class Dispatcher(object):
    
    def __init__(self, queue_name):
        self.queue_name = queue_name
        self.in_flight_messages = {}
        bus = get_bus()
        bus.add_listener(self.queue_name, self.on_reply)

    def dispatch(self, payload):
        message_id = str(uuid.uuid4())
        self.in_flight_messages[message_id] = { "attempts": 1, "dispatched": datetime.datetime.now() }
        print (F'sending {payload} to {self.queue_name}')
        bus = get_bus()
        bus.dispatch(self.queue_name, str(payload))

    def on_reply(self, payload):
        print("I got this message in response")
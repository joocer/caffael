"""
Dispatcher
"""

import uuid
import datetime

class Dispatcher(object):
    
    def __init__(self, queue_name):
        self.queue_name = queue_name
        self.in_flight_messages = {}

    def emit(self, payload):
        message_id = str(uuid.uuid4())
        self.in_flight_messages[message_id] = { "attempts": 1, "dispatched": datetime.datetime.now() }
        print (F'fake sending {payload} to {self.queue_name}')
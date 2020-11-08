from caffael.worker.resources.mqtt import MQTT

def handler(payload):
    print(payload)
    return payload

m = MQTT('interval_5s', handler)
m.connect()

import time

while True:
    time.sleep(60)
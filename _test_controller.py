from caffael.controller import Scheduler, Dispatcher, MQTT
from caffael.controller.triggers import IntervalTrigger
import time
import yaml

def read_config(config_file):
    with open(config_file, 'r') as f:
        yaml_config = yaml.load(f, Loader=yaml.BaseLoader)
    return yaml_config

config = read_config("caffael.yaml")
mqtt = MQTT(config['mqtt'])

scheduler = Scheduler()

# create a trigger and dispatcher
interval_5s_dispatcher = Dispatcher(queue_name="interval_5s")
interval_5s_trigger = IntervalTrigger(polling_interval=1, 
    interval=5, 
    max_runs=10, 
    dispatcher=interval_5s_dispatcher)
scheduler.add_event(interval_5s_trigger)

# create a second trigger and dispatcher
interval_15s_dispatcher = Dispatcher(queue_name="interval_15s")
interval_15s_trigger = IntervalTrigger(polling_interval=1, 
    interval=15, 
    max_runs=5, 
    dispatcher=interval_15s_dispatcher)
scheduler.add_event(interval_15s_trigger)

scheduler.execute()

while scheduler.running():
    print('Scheduler Still Alive')
    time.sleep(10)

print('EOS')
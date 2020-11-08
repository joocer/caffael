from caffael.controller import Scheduler, Dispatcher
from caffael.controller.triggers import IntervalTrigger, CronTrigger
from caffael.controller.resources import get_bus
import time


scheduler = Scheduler()

# create a trigger and dispatcher
interval_5s_dispatcher = Dispatcher(queue_name="interval_5s")
interval_5s_trigger = IntervalTrigger(polling_interval=1, 
    interval=5, 
    max_runs=-1, # run forever
    dispatcher=interval_5s_dispatcher)
scheduler.add_event(interval_5s_trigger)

scheduler.execute()

while scheduler.running():
    print('Scheduler Still Alive')
    time.sleep(10)

print('EOS')
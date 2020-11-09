from caffael.controller import Scheduler
from caffael.controller.dispatchers import PrintToScreenDispatcher
from caffael.controller.triggers import IntervalTrigger, CronTrigger, SimpleHTTPTrigger, FileWatchTrigger
from caffael.controller.resources import get_bus
import time


scheduler = Scheduler()

# create a trigger and dispatcher
dispatcher = PrintToScreenDispatcher()
interval_5s_trigger = IntervalTrigger(polling_interval=1,
    interval=5,
    max_runs=-1, # run forever
    dispatcher=dispatcher)
scheduler.add_trigger(interval_5s_trigger)

http_trigger = SimpleHTTPTrigger(dispatcher=dispatcher)
scheduler.add_trigger(http_trigger)

file_watch_trigger = FileWatchTrigger(filename="%Y.txt", 
    max_runs=-1,
    dispatcher=dispatcher)
scheduler.add_trigger(file_watch_trigger)

scheduler.execute()

while scheduler.running():
    print('Scheduler Still Alive')
    time.sleep(10)

print('EOS')
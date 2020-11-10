from caffael import Scheduler
from caffael.dispatchers import PrintToScreenDispatcher
from caffael.triggers import IntervalTrigger, CronTrigger, SimpleHTTPTrigger, FileWatchTrigger
from caffael.resources import get_bus
import time


scheduler = Scheduler()

# create a trigger and dispatcher
dispatcher = PrintToScreenDispatcher(label="test dispatcher")

interval_5s_trigger = IntervalTrigger(polling_interval=1,
    interval=5,
    dispatcher=dispatcher)
scheduler.add_trigger(interval_5s_trigger)

http_trigger = SimpleHTTPTrigger(dispatcher=dispatcher)
scheduler.add_trigger(http_trigger)

file_watch_trigger = FileWatchTrigger(filename="%Y.txt",
    dispatcher=dispatcher)
scheduler.add_trigger(file_watch_trigger)

scheduler.execute()

while scheduler.running():
    print('Scheduler Still Alive')
    time.sleep(10)

print('EOS')
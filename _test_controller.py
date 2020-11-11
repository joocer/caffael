from caffael import Scheduler
from caffael.dispatchers import PrintToScreenDispatcher
from caffael.triggers import IntervalTrigger, SimpleHTTPTrigger
import time
import datetime


scheduler = Scheduler()

# create a dispatcher, in this case it's the demo print dispatcher
dispatcher = PrintToScreenDispatcher(label="test dispatcher")

# create a trigger, assign the dispatcher and add to the scheduler
interval_5s_trigger = IntervalTrigger(interval=5, dispatcher=dispatcher)
scheduler.add_trigger(interval_5s_trigger)

# create another trigger, asign the same (or a different) dispatcher
# and add to the scheduler
http_trigger = SimpleHTTPTrigger(dispatcher=dispatcher)
scheduler.add_trigger(http_trigger)

# start the scheduler
scheduler.execute()

# the scheduler should run forever, print a heart-beat every 15 mins
while scheduler.running():
    print('Scheduler Still Alive @ ', datetime.datetime.now().isoformat())
    time.sleep(900)

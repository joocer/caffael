import threading
import time
from ..exceptions import StopTrigger
#from ..http import api_initializer

def _schedule_thread_runner(trigger):
    """
    The wrapper around triggers, this is blocking so should be
    run in a separate thread.

    - Memory and Keyboard Errors are bubbled.
    - StopTriggers gracefully
    - Other errors are ignored
    """
    keep_running_trigger = True

    while keep_running_trigger:
        try:
            print('engage the trigger')
            trigger.engage()
        except KeyboardInterrupt:
            raise KeyboardInterrupt()
        except MemoryError:
            raise MemoryError()
        except StopTrigger:
            keep_running_trigger = False
        # don't form a tight loop, slow it down
        time.sleep(5)
    print(f"Scheduler Thread {threading.current_thread().get_name()} has died")


class Scheduler(object):
    """
    Scheduler allows multiple pipelines to be run.

    Scheduled tasks must have a trigger, this trigger will acquire
    the initializing data for the flow.
    """
    def __init__(self): #, enable_api=True, api_port=8000):
        self._threads = []
        #if enable_api:
        #    # the very start of the HTTP Interface
        #    api_thread = threading.Thread(target=api_initializer, args=(self, api_port))
        #    api_thread.daemon = True
        #    api_thread.setName("cronicl:api_thread")
        #    api_thread.start()

    def add_event(self, trigger):
        event_thread = threading.Thread(
            target=_schedule_thread_runner, args=(trigger,)
        )
        event_thread.daemon = True
        event_thread.setName(F"scheduler:{trigger.__class__.__name__}")
        self._threads.append(event_thread)

    def execute(self):
        """
        Start each of the flow trigger threads
        """
        [t.start() for t in self._threads]

    def running(self):
        """
        Are any thread still running
        """
        return any([t.is_alive() for t in self._threads])

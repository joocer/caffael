import abc
from ..exceptions import StopTrigger
import datetime
import time


class BaseTrigger(abc.ABC):
    """
    Base Trigger
    """
    def __init__(self, *args, **kwargs):

        self.dispatcher = kwargs.get('dispatcher')

    def set_flow(self, flow):
        """
        Set the flow this trigger should feed data to
        """
        self.flow = flow

    @abc.abstractmethod
    def engage(self, flow, logging):
        """
        'engage' is called when a trigger is loaded.
        This should start any listening activities - like 
        subscribing to message queues. 
        """
        raise NotImplementedError("'engage' must be overridden")

    def on_event(self, *args, **kwargs):
        """
        DO NOT OVERRIDE THIS METHOD
        """
        self.flow.execute(*args, **kwargs)


class BasePollingTrigger(BaseTrigger):
    """
    Base Polling Trigger
    parameters
    - interval: the number of seconds between polls
    - max_runs: the number of times to execute the flow from this
                trigger, -1 = run forever
    """

    def __init__(self, *args, **kwargs):
        """
        max runs < 0 = run until stopped
        """
        super(BasePollingTrigger, self).__init__(*args, **kwargs)
        self.polling_interval = kwargs.get('polling_interval', 60)
        self.max_runs = kwargs.get('max_runs', -1)


    @abc.abstractmethod
    def nudge(self):
        """
        This must call on_event with the data to pass to the
        pipeline.
        This method shouldn't return anything.
        """
        raise NotImplementedError("'nudge' must be overridden")

    def engage(self, logging):
        """
        Built in
        """
        self.logging = logging
        while self.max_runs != 0:
            self.nudge()
            time.sleep(self.polling_interval)
        raise StopTrigger('Max runs completed')

    def on_event(self, *args, **kwargs):
        """
        DO NOT OVERRIDE THIS METHOD
        """
        self.max_runs -= 1
        self.dispatcher.emit(*args, **kwargs)
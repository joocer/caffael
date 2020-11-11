
from .base_trigger import BasePollingTrigger
import datetime


class IntervalTrigger(BasePollingTrigger):
    """
    Trigger based on an interval
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.interval = kwargs.get('interval', 60)
        if type(self.interval).__name__ == "int":
            # if a number, treat as seconds
            self.interval = datetime.timedelta(seconds=self.interval)
        elif not type(self.interval).__name__ == "timedelta":
            raise TypeError(
                "Interval must be either a number of seconds or a timedelta"
            )
        if self.label:
            self.label = self.label + " - " + str(int(self.interval.total_seconds())) + "s"
        else:
            self.label = str(int(self.interval.total_seconds())) + "s"

    def nudge(self):
        """
        test if the condition to run has been met
        """
        self.on_event(datetime.datetime.now().isoformat())

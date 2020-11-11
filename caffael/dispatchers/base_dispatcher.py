import abc


class BaseDispatcher(abc.ABC):

    def __init__(self, *args, **kwargs):
        self.label = kwargs.get('label')

    @abc.abstractmethod
    def on_event(self, *arg, **kwargs):
        raise NotImplementedError("Dispatcher 'on_event' must be overriden.")

    def on_completion(self, *arg, **kwargs):
        raise NotImplementedError("Dispatcher 'on_completion' must be overriden.")

    def __str__(self):
        if self.label:
            return f"{self.__class__.__name__} ({self.label})"
        return f"{self.__class__.__name__}"

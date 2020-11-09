import abc


class BaseDispatcher(abc.ABC):

    @abc.abstractmethod
    def on_event(self, *arg, **kwargs):
        raise NotImplementedError("Dispatcher 'on_event' must be overriden.")

    def on_completion(self, *arg, **kwargs):
        raise NotImplementedError("Dispatcher 'on_reply' must be overriden.")

from .base_dispatcher import BaseDispatcher


class PrintToScreenDispatcher(BaseDispatcher):
    """
    This dispatcher is intended for testing purposes only.

    Rather than dispatch a message to another service, this just
    writes the payload to the screen.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_event(self, payload):
        print(str(payload))
        self.on_completion(payload)

    def on_completion(self, value):
        pass

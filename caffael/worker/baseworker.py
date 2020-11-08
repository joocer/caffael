

class BaseWorker(object):

    def __init__(self):
        pass

    def acquire(self, message):
        return message

    def pre_validate(self, payload):
        return True

    def process(self, payload):
        return payload

    def post_validate(self, payload):
        return True

    def execute(self, message):

        payload = self.acquire(message)

        if not self.pre_validate(payload):
            raise Exception("not a valid payload")

        payload = self.process(payload)

        if not self.post_validate(payload):
            raise Exception("not a valid payload")



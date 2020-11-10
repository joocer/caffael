from .base_dispatcher import BaseDispatcher
import subprocess
import warnings


class CommandLineDispatcher(BaseDispatcher):
    """
    A simple dispatcher which executes the command line.

    init([command])
    on_event(payload)
    => command payload
    """
    def __init__(self, command):
        warnings.warn("CommandLineDispatcher is not safe for production systems.")
        self.command = command

    def on_event(self, payload):
        my_command = self.command.copy()
        if payload:
            my_command.append(payload)
        result = subprocess.run(my_command, stdout=subprocess.PIPE)
        result = result.stdout.decode('utf8').rstrip('\n')
        self.on_completion(result)

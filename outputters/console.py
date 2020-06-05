import json


class ConsoleOutput:
    """Default to print output back to the console"""
    def __init__(self, **kwargs):
        pass

    def send(self, data):
        for finding in data:
            print(json.dumps(finding, indent=4))

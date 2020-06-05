from outputters import *


class OutputterFactory:
    """Factory class to facilitate creation and use of different storage mediums for parsed Nessus data"""

    def __init__(self):
        self._outputters = {}

    def register(self, title, new_outputter):
        """Add the new_ouputter class to our dict prior to attempting to use it"""
        self._outputters[title] = new_outputter

    def get(self, title, **kwargs):
        """Get the Outputter itself and instantiate it with whatever credentials it requires"""
        out = self._outputters.get(title)
        if not out:
            raise ValueError('{} is not registered in the factory, '
                             'create the Outputter class and register it.'.format(title))
        return out(**kwargs)


outputter = OutputterFactory()
outputter.register('postgres', Postgres)
outputter.register('elasticsearch', Elastic)
outputter.register('splunk', Splunk)
outputter.register('default', ConsoleOutput)

from outputters import *


class OutputterFactory:

    def __init__(self):
        self._outputters = {}

    def register(self, title, new_outputter):
        self._outputters[title] = new_outputter

    def get(self, title, **kwargs):
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

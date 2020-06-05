from plugins import *


class PluginFactory:

    def __init__(self):
        self._plugins = {}

    def register(self, plugin_id, new_plugin):
        self._plugins[plugin_id] = new_plugin

    def get(self, plugin_id):
        plugin_parser = self._plugins.get(plugin_id)
        if not plugin_parser:
            plugin_parser = DefaultPluginParser
        return plugin_parser()


plugin = PluginFactory()
# Register Plugin ID and Plugin Parser
plugin.register(20811, WindowsSoftwarePlugin)

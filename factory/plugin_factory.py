from plugins import *


class PluginFactory:
    """Factory class to facilitate adding custom parsers for specific Nessus plugins as desired"""

    def __init__(self):
        self._plugins = {}

    def register(self, plugin_id, new_plugin):
        """Register the new plugin prior to attempting to parse Nessus output with it using its Nessus plugin ID"""
        self._plugins[plugin_id] = new_plugin

    def get(self, plugin_id):
        """Get the proper Plugin parser for the plugin id supplied, or return the Default parser"""
        plugin_parser = self._plugins.get(plugin_id)
        if not plugin_parser:
            plugin_parser = DefaultPluginParser
        return plugin_parser()


plugin = PluginFactory()
plugin.register(20811, WindowsSoftwarePlugin)

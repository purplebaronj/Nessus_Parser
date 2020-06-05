import re


class WindowsSoftwarePlugin:
    def parse(self, plugin_output):
        stop_point = plugin_output.find('The following updates are installed')
        start_point = plugin_output.find('\n')
        software_listing = plugin_output[start_point:stop_point]
        for k in re.findall(r'(.*)(\[version\s(.*)\])', software_listing):
            yield {'Software': k[0].rstrip(), 'Version': k[2].split('] ')[0]}

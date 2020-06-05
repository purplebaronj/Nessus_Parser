from configparser import ConfigParser
from factory import outputter, plugin
from plugins import DefaultPluginParser
from xml.etree import ElementTree as ET

import argparse
import glob
import json
import logging
import os

log = logging.getLogger(__name__)


class NessusParser:

    def __init__(self, nessus_report, outputter):
        self.filename = nessus_report
        self.outputter = outputter

    def _parse(self):
        log.info('Nessus Parser processing {}'.format(self.filename))
        report_name = os.path.basename(self.filename.split('.nessus')[0])
        for event, elem in ET.iterparse(self.filename):
            if elem.tag == 'Policy':
                elem.clear()
            if elem.tag == 'HostProperties':
                props_dict = {prop.get('name'): prop.text for prop in iter(elem)}
                elem.clear()
                props_dict['Report Name'] = report_name
                props_dict['File Name'] = self.filename

            elif elem.tag == 'ReportItem':
                event_dict = {}
                event_dict.update(elem.attrib)
                # Log Nessus Auth failures, otherwise disregard "Settings" findings
                if event_dict['pluginFamily'] == 'Settings':
                    if 'Authentication Failure' in event_dict['pluginName']:
                        log.warning('Nessus failed to authenticate to host {} in {}'.format(props_dict['host-ip'],
                                                                                            self.filename))
                    continue
                else:
                    event_dict.update({item.tag: item.text for item in iter(elem)})
                    plugin_id = event_dict['pluginID']
                    current_plugin = plugin.get(plugin_id)
                    if isinstance(current_plugin, DefaultPluginParser):
                        yield json.dumps(event_dict)
                    else:
                        for data in current_plugin.parse(elem.find('plugin_output').text):
                            data.update(event_dict)
                            yield json.dumps(data)
                elem.clear()
                del event_dict

    def parse(self):
        self.outputter.send((event for event in self._parse()))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse Nessus scan files and send the output to your favorite backend.')
    parser.add_argument('--directory', metavar='directory', default='.', help='Directory containing .nessus scan files to parse')
    parser.add_argument('--scan', metavar='scan', default=None, help='Path to Nessus scan file if only one is to be parsed')
    parser.add_argument('--netstat', dest='netstat', default=True, action='store_true', help='Process Netstat Entries')
    parser.add_argument('--config', metavar='config', default='.parser_config', help='Config file with credentials to desired outputter')
    args = parser.parse_args()

    if not os.path.exists(args.config):
        log.warning('Config file for desired outputter does not exist. Defaulting to console output.')
        output = outputter.get('default')
    else:
        config = ConfigParser(interpolation=None)
        config.read(args.config)
        conf = config['Credentials']
        conf['Title'] = conf['Title'].lower()
        output = outputter.get(**conf)

    scan_files = glob.glob(os.path.join(args.directory, "*.nessus"))
    if not scan_files:
        raise ValueError(f'No .nessus files found to parse in {os.path.abspath(args.directory)}')

    for f in scan_files:
        try:
            NessusParser(f, output).parse()
        except Exception as e:
            log.error(f'Error parsing {f}. {e}')


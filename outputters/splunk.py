import logging
import splunklib.client as client

log = logging.getLogger(__name__)


class Splunk:
    """Class to allow parsed data to be sent into a Splunk index"""

    def __init__(self, user, password, index, host, port=8089):
        self.service = client.connect(host=host,
                                      port=port,
                                      username=user,
                                      password=password,
                                      autologin=True,
                                      )
        if index not in self.service.indexes:
            self.service.indexes.create(index)
        self.index = self.service.indexes[index]

    def send(self, data):
        """Send data to Splunk Index"""
        with self.index.attached_socket(sourcetype='Nessus') as sock:
            for event in data:
                event_bytes = event + '\r\n'
                sock.send(event_bytes.encode('utf-8'))
        log.info(f'Sent to Splunk - {self.index}')

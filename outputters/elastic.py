from elasticsearch import Elasticsearch

import logging

log = logging.getLogger(__name__)


class Elastic:
    """Class to send parsed data into an ElasticSearch index"""

    def __init__(self, index, user=None, password=None, cloud_id=None, host='localhost', port=9200):
        if user and password:
            self.es = Elasticsearch([host, ], port=port, http_auth=(user, password))
        elif cloud_id:
            self.es = Elasticsearch(cloud_id=cloud_id, http_auth=(user, password))
        else:
            self.es = Elasticsearch([host, ], port=port)
        self.index = index
        self.es.indices.create(index=self.index, ignore=400)

    def send(self, data):
        """Add data to Elastic Index"""
        # TODO: Implement Bulk API to send data in larger streams
        for event in data:
            self.es.index(index=self.index, doc_type="nessus_scans", body=event)
        log.info(f'Sent to Elastic - {self.index}')

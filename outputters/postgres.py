import logging
import psycopg2

log = logging.getLogger(__name__)


class Postgres:
    """Class to allow parsed data to be send into a Postgres table"""

    def __init__(self, user, password, database, host='127.0.0.1', port=5432):
        self.conn = psycopg2.connect(database=database, host=host, port=port, user=user, password=password)
        self.cur = None

    def _create_table(self):
        """Create basic table to store all data in JSON field"""
        self.cur.execute("CREATE TABLE IF NOT EXISTS nessus (id SERIAL, report_obj JSONB, src_file TEXT, "
                         "PRIMARY KEY (id));"
        )

    def send(self, data):
        """Create table as necessary and send data into Postgres"""
        with self.conn.cursor() as self.cur:
            self._create_table()
            # TODO Change this to use execute_batch instead to make it more performant
            for event in data:
                f = event.pop('File Name')
                self.cur.execute("INSERT INTO nessus (report_obj, src_file) VALUES (%(json_obj)s, %(src_file)s);",
                                 {"json_obj": event, "src_file": f})

        self.conn.commit()
        log.info('Data sent to Postgres')

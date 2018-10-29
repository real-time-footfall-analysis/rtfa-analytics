import os

# Configuration dictionary.
import psycopg2 as psycopg2

from utils.heatmap_generator import HeatmapGenerator
from utils.person_tracker import PersonTracker

DEFAULT_LOG_TABLE_NAME = "log"

DEFAULT_CONFIG = {
    'dbname': 'log',
    'user': os.environ['RTFA-REDSHIFT-USR'],
    'pwd': os.environ['RTFA-REDSHIFT-PWD'],
    'host': 'movement-log.cnadblxzqjnp.eu-central-1.redshift.amazonaws.com',
    'port': '5439'
}


class RedshiftRetriever:

    # Used to retrieve events from AWS Redshift database. Parses them to objects from utils/state.

    def __init__(self, event_id, config=None, log_table_name=None):
        self.config = DEFAULT_CONFIG if config is None else config
        self.event_id = event_id
        self.log_table_name = DEFAULT_LOG_TABLE_NAME if log_table_name is None else log_table_name

    def __connect_and_execute(self, sql):
        # Creates a connection to the Redshift database, executes query, closes connection and returns result.
        config = self.config
        connection = psycopg2.connect(dbname=config['dbname'], host=config['host'], port=config['port'],
                                      user=config['user'],
                                      password=config['pwd'])
        cursor = connection.cursor()

        # Make sql request and store results.
        cursor.execute(sql)
        rows = cursor.fetchall()

        # Close connection and return.
        cursor.close()
        connection.close()
        return rows

    def retrieve_event_movements(self, time_start=None, time_end=None):
        # Retrieves and returns movements of all people from start (inclusive) to end (exclusive), or ever if left None.

        # Generate SQL statement.
        fields = ", ".join(["uuid", "\"timestamp\"", "regionId", "entering"])

        constraints = "eventId=%s" % self.event_id
        constraints += " AND timestamp >= %s" % time_start if time_start is not None else ""
        constraints += " AND timestamp < %s" % time_end if time_end is not None else ""
        sql = "SELECT %s FROM %s WHERE %s" % (fields, self.log_table_name, constraints)
        rows = self.__connect_and_execute(sql)

        return rows

    def retrieve_person_movements(self, uid):
        # Retrieves and returns movements for a given person uid.

        # Generate SQL and execute statement.
        fields = ", ".join(["\"timestamp\"", "regionId", "entering"])
        constraints = "eventId=%s AND uuid=\"%s\"" % (self.event_id, uid)
        sql = "SELECT %s FROM %s WHERE %s" % (fields, self.log_table_name, constraints)
        rows = self.__connect_and_execute(sql)

        return rows

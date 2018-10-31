import os

# Configuration dictionary.
import psycopg2 as psycopg2
from typing import Set

from interface.static_data_interface import StaticDataInterface

DEFAULT_ENABLED_EVENT_TASKS_TABLE = "event_tasks"


class StaticDataRetriever(StaticDataInterface):
    # Used to retrieve static data from AWS RDS.

    def __init__(self, config=None, enabled_event_tasks_table=None):
        super().__init__()

        default_config = {
            'dbname': 'rtfa_crowd_static_data',
            'user': os.environ['CROWD_STATIC_USR'],
            'pwd': os.environ['CROWD_STATIC_PWD'],
            'host': 'rtfa-crowd-static-data.chh9za0s2bso.eu-central-1.rds.amazonaws.com',
            'port': '5432'
        }

        self.config = default_config if config is None else config
        self.enabled_event_tasks_table = DEFAULT_ENABLED_EVENT_TASKS_TABLE \
            if enabled_event_tasks_table is None else enabled_event_tasks_table

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

    # Returns set of event_ids that are currently running.
    def get_running_events(self) -> Set:
        # TODO: Link this to a table.
        return {1, 2}

    # Returns set of enabled task ids for a particular event.
    def get_enabled_tasks(self, event_id) -> Set:
        sql = "SELECT tasks FROM %s WHERE event_id=%s" % (self.enabled_event_tasks_table, event_id)
        tasks = self.__connect_and_execute(sql)
        return set(tasks[0][0])

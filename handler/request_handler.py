from interface.destination_interface import DestinationInterface
from interface.dynamo_writer import DynamoWriter
from interface.log_interface import LogInterface
from interface.redshift_retriever import RedshiftRetriever
from interface.state_interface import StateInterface
from interface.state_retriever import StateRetriever
from interface.static_data_interface import StaticDataInterface
from interface.static_data_retriever import StaticDataRetriever
from tasks.task_mappings import FREQUENCY_GROUPS, TASK_IDS


class RequestHandler:
    def __init__(self, state_data=None, static_data_source=None, log_source=None, data_dest=None):
        self.state_data: StateInterface = StateRetriever() if state_data is None else state_data
        self.static_data_source: StaticDataInterface = StaticDataRetriever() if static_data_source is None else static_data_source
        self.log_source: LogInterface = RedshiftRetriever() if log_source is None else log_source
        self.data_dest: DestinationInterface = DynamoWriter() if data_dest is None else data_dest

    def execute_tasks(self, frequency_group):
        # Retrieves enabled tasks within frequency group, and executes them, for each live event.

        tasks_in_frequency_group = FREQUENCY_GROUPS[frequency_group]
        live_events = self.static_data_source.get_running_events()

        # Go through live events, execute valid tasks.
        for event_id in live_events:

            # Find intersection of enabled tasks for event, and tasks in frequency group.
            enabled_task_ids = self.static_data_source.get_enabled_tasks(event_id)
            executables = enabled_task_ids & tasks_in_frequency_group
            for task_id in executables:
                task = TASK_IDS[task_id]

                # Create and execute task.
                executor = task(self.state_data, self.log_source, self.static_data_source, task_id)
                result = executor.execute(event_id)

                # Update results table with new object.
                print(result)
                #self.data_dest.update_object(task_id, event_id, result)

        return True

r = RequestHandler()
r.execute_tasks(5)
from interface.destination_interface import DestinationInterface
from interface.log_interface import LogInterface
from interface.redshift_retriever import RedshiftRetriever
from interface.static_data_interface import StaticDataInterface
from tasks.task_mappings import FREQUENCY_GROUPS, TASK_IDS


class RequestHandler:
    def __init__(self, static_data_source=None, log_source=None, data_dest=None):
        # TODO: These None values will be replaced.
        self.static_data_source: StaticDataInterface = None if static_data_source is None else static_data_source
        self.log_source: LogInterface = RedshiftRetriever() if log_source is None else log_source
        self.data_dest: DestinationInterface = None if data_dest is None else data_dest

    def execute_tasks(self, frequency_group):
        # Retrieves enabled tasks within frequency group, and executes them, for each live event.

        tasks_in_frequency_group = FREQUENCY_GROUPS[frequency_group]

        live_events = self.static_data_source.get_running_events()

        for event_id in live_events:
            enabled_task_ids = self.static_data_source.get_enabled_tasks(event_id)
            executables = enabled_task_ids & tasks_in_frequency_group

            for id in executables:
                task = TASK_IDS[id]

                result = task(self.log_source, event_id)
                self.data_dest.update_object(id, event_id, result)

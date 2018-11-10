from interface.log_interface import LogInterface
from interface.state_interface import StateInterface
from interface.static_data_interface import StaticDataInterface


class Task:
    def __init__(self, state_data: StateInterface, log_source: LogInterface, static_data_source: StaticDataInterface,
                 task_id):
        self.state_data = state_data
        self.log_source = log_source
        self.static_data_source = static_data_source
        self.task_id = task_id

    def execute(self, event_id): pass

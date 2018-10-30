from typing import Dict


class DestinationInterface:
    def __init__(self): pass

    def update_object(self, task_id, event_id, json_obj: Dict): pass

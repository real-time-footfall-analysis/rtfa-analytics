from typing import Set


class StaticDataInterface:

    def __init__(self): pass

    # Returns set of event_ids that are currently running.
    def get_running_events(self) -> Set: pass

    # Returns set of enabled task ids for a particular event.
    def get_enabled_tasks(self, event_id) -> Set: pass
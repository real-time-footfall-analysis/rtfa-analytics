from typing import Set, Dict


class StaticDataInterface:
    def __init__(self): pass

    # Returns set of event_ids that are currently running.
    def get_running_events(self) -> Set: pass

    # Returns set of enabled task ids for a particular event.
    def get_enabled_tasks(self, event_id) -> Set: pass

    # Returns all regions for a event.
    def get_regions(self, event_id) -> Set: pass

    # Returns particular attribute for all regions for an event.
    def get_region_attribute(self, event_id, attribute) -> Dict: pass

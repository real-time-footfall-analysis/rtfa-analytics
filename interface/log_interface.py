from typing import List, Tuple

class LogInterface:

    def __init__(self): pass

    def retrieve_event_movements(self, event_id, time_start: int=None, time_end: int=None) -> List[Tuple]: pass

    def retrieve_person_movements(self, event_id, uid: int) -> List[Tuple]: pass

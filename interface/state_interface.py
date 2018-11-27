class StateInterface:
    def __init__(self): pass

    def get_task_state(self, task_id, event_id): pass

    def save_task_state(self, task_id, event_id, state): pass

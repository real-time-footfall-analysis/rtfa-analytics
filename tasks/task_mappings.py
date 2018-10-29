from tasks import dummy_task
from typing import Callable, Dict

# Maps task ids to task definitions, used to find enabled tasks for a particular event,
TASK_IDS: Dict[int, Callable[..., Dict]] = {
    1: dummy_task
}

# Maps frequency groups to set of task_ids to be executed at particular frequency.
FREQUENCY_GROUPS = {
    5: {1}
}

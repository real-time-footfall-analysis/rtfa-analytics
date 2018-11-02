from tasks.average_queue_time import average_queue_time
from tasks.average_stay_time import average_stay_time
from typing import Callable, Dict

# Maps task ids to task definitions, used to find enabled tasks for a particular event,
TASK_IDS: Dict[int, Callable[..., Dict]] = {
    1: average_stay_time,
    3: average_queue_time,
}

# Maps frequency groups to set of task_ids to be executed at particular frequency.
FREQUENCY_GROUPS = {
    5: {1, 3}
}

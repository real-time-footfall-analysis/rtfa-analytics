from tasks import Task
from tasks.average_queue_time import AverageQueueTime
from tasks.average_stay_time import AverageStayTime
from tasks.bounce_rate import BounceRate
from typing import Callable, Dict

# Maps task ids to task definitions, used to find enabled tasks for a particular event,
TASK_IDS = {
    1: AverageStayTime,
    2: BounceRate,
    3: AverageQueueTime,
}

# Maps frequency groups to set of task_ids to be executed at particular frequency.
FREQUENCY_GROUPS = {
    5: {1, 2, 3}
}

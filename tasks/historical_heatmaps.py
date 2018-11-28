import time

import math

from tasks.task import Task
from utils.heatmap_generator import HeatmapGenerator

DEFAULT_TIME_INTERVAL = 300


class HistoricalHeatmaps(Task):
    def __init__(self, state_data, log_source, static_data_source, task_id):
        super().__init__(state_data, log_source, static_data_source, task_id)

    def execute(self, event_id):
        heatmap_gen = self.state_data.get_task_state(self.task_id, event_id)
        if heatmap_gen is not None:
            # Get all movements since last movement, not including what has occurred in the current second.
            last_movement = heatmap_gen.last_movement if heatmap_gen.last_movement else -1
            movements_since_last_update = self.log_source.retrieve_event_movements(event_id, time_start=last_movement+1,
                                                                                   time_end=math.floor(time.time()))
            heatmap_gen.append_movements(movements_since_last_update)
        else:
            event_movements = self.log_source.retrieve_event_movements(event_id)
            heatmap_gen = HeatmapGenerator(event_id, event_movements)

        times, heatmaps = heatmap_gen.build_heat_map_history(time_interval=DEFAULT_TIME_INTERVAL)
        result = {"timestamps": times, "data": heatmaps}

        # Save new heatmap generator state.
        self.state_data.save_task_state(self.task_id, event_id, heatmap_gen)
        return result

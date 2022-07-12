from enum import Enum


class TasksStatus(str, Enum):
    all = 'all'
    done = 'done'
    in_progress = "in_progress"

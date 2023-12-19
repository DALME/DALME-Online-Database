"""Interface for the dalme_api.resources.tasks module."""
from .endpoints import TaskLists, Tasks
from .serializers import TaskListSerializer, TaskSerializer

__all__ = [
    'Tasks',
    'TaskLists',
    'TaskListSerializer',
    'TaskSerializer',
]

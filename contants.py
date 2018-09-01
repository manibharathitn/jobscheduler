from enum import Enum
class JobType(Enum):
    SCHEDULED_JOB = 'Scheduled Job'
    EVENT_JOB = 'Event Job'

class JobStatus(Enum):
    SUCCESS = 'Success'
    FAILED = 'Failed'
    RUNNING = 'Running'
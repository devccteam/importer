from enum import Enum


class status(Enum):
    pending = {'status': 'PENDING'}

    started = {'status': 'STARTED'}

    success = {'status': 'SUCCESS'}

    failure = {'status': 'FAILURE'}

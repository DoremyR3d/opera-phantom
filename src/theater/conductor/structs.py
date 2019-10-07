from datetime import datetime
from multiprocessing import Process, Queue

import attr

from theater.core.messages import Status

__all__ = ['ManagedComponent']


@attr.s
class ManagedComponent:
    name = attr.ib(type=str)
    uuid = attr.ib(type=str)
    process = attr.ib(type=Process)
    queue = attr.ib(type=Queue)
    beattime = attr.ib(type=datetime)
    status = attr.ib(type=Status)

from datetime import datetime
from multiprocessing import Process

import attr

from theater.core.messages import Status, ProducerQueue

__all__ = ['ManagedComponent']


@attr.s
class ManagedComponent:
    name = attr.ib(type=str)
    uuid = attr.ib(type=str)
    process = attr.ib(type=Process)
    queue = attr.ib(type=ProducerQueue)
    beattime = attr.ib(type=datetime)
    status = attr.ib(type=Status)

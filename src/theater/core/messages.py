import multiprocessing.queues
from datetime import datetime
from typing import Optional, Tuple

import attr

from theater.core.constants import Signal, MsgType
from theater.core.errors import IllegalActionException

__all__ = ['Message', 'Status', 'generatequeues']


@attr.s(kw_only=True, frozen=True)
class Status:
    reqtime = attr.ib(type=Optional[datetime],
                      validator=attr.validators.optional(attr.validators.instance_of(datetime)))
    status = attr.ib(type=Optional[str],
                     validator=attr.validators.optional(attr.validators.instance_of(str)))
    time = attr.ib(type=Optional[datetime],
                   validator=attr.validators.optional(attr.validators.instance_of(datetime)))
    statustime = attr.ib(type=Optional[datetime],
                         validator=attr.validators.optional(attr.validators.instance_of(datetime)))
    statusmessage = attr.ib(type=Optional[str],
                            validator=attr.validators.optional(attr.validators.instance_of(str)))


@attr.s(kw_only=True, frozen=True)
class Message:
    sender = attr.ib(type=str, validator=attr.validators.instance_of(str))
    signal = attr.ib(type=Signal, validator=attr.validators.instance_of(Signal))
    type = attr.ib(type=MsgType, validator=attr.validators.instance_of(MsgType))
    extension = attr.ib(default={}, type=dict, validator=attr.validators.instance_of(dict))
    body = attr.ib()

    @body.validator
    def body_validator(self, _, instance):
        if self.type is None:
            raise TypeError("You can't add a body without first specifying its type!")
        elif self.type is MsgType.TEXT:
            if not isinstance(instance, str):
                raise TypeError("A type TEXT requires a str body")
        elif self.type is MsgType.STATUS:
            if not isinstance(instance, Status):
                raise TypeError("A type STATUS requires a dict body")
        elif self.type is MsgType.BYTES:
            if not isinstance(instance, bytes):
                raise TypeError("A type BYTES requires a bytes body")
        elif self.type is MsgType.MAP:
            if not isinstance(instance, dict):
                raise TypeError("A type MAP requires a dict body")
        elif self.type is MsgType.NONE:
            if instance:
                raise TypeError("A type NONE requires a None body")
        else:
            raise ValueError("This type of message isn't supported")


class ProducerQueue(multiprocessing.queues.Queue):
    __slots__ = ('__innerq',)

    def __init__(self, innerq: multiprocessing.queues.Queue):
        if not isinstance(innerq, multiprocessing.queues.Queue):
            raise TypeError
        self.__innerq = innerq

    def put(self, obj, block: bool = ..., timeout: Optional[float] = ...) -> None:
        self.__innerq.put(obj, block, timeout)

    def qsize(self) -> int:
        return self.__innerq.qsize()

    def empty(self) -> bool:
        return self.__innerq.empty()

    def full(self) -> bool:
        return self.__innerq.full()

    def put_nowait(self, item) -> None:
        self.__innerq.put_nowait(item)

    def close(self) -> None:
        self.__innerq.close()

    def join_thread(self) -> None:
        self.__innerq.join_thread()

    def cancel_join_thread(self) -> None:
        self.__innerq.cancel_join_thread()

    def join(self) -> None:
        self.__innerq.join()

    def task_done(self) -> None:
        self.__innerq.task_done()

    def get(self, block: bool = ..., timeout: Optional[float] = ...):
        raise IllegalActionException()

    def get_nowait(self):
        raise IllegalActionException()


class ConsumerQueue(multiprocessing.queues.Queue):
    __slots__ = ('__innerq',)

    def __init__(self, innerq: multiprocessing.queues.Queue):
        if not isinstance(innerq, multiprocessing.queues.Queue):
            raise TypeError
        self.__innerq = innerq

    def put(self, obj, block: bool = ..., timeout: Optional[float] = ...) -> None:
        raise IllegalActionException()

    def qsize(self) -> int:
        return self.__innerq.qsize()

    def empty(self) -> bool:
        return self.__innerq.empty()

    def full(self) -> bool:
        return self.__innerq.full()

    def put_nowait(self, item) -> None:
        raise IllegalActionException()

    def close(self) -> None:
        self.__innerq.close()

    def join_thread(self) -> None:
        self.__innerq.join_thread()

    def cancel_join_thread(self) -> None:
        self.__innerq.cancel_join_thread()

    def join(self) -> None:
        self.__innerq.join()

    def task_done(self) -> None:
        self.__innerq.task_done()

    def get(self, block: bool = ..., timeout: Optional[float] = ...):
        return self.__innerq.get(block, timeout)

    def get_nowait(self):
        return self.__innerq.get_nowait()


def generatequeues() -> Tuple[ProducerQueue, ConsumerQueue]:
    innerq = multiprocessing.Queue()
    return ProducerQueue(innerq), ConsumerQueue(innerq)

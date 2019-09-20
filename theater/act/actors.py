import multiprocessing
import time
from abc import ABC, abstractmethod
from datetime import datetime
from queue import Empty
from typing import Callable, Union

from theater.act.errors import IllegalValueException
from theater.act.messages import Message, MessageFactory, Signal, MsgType

__all__ = ['Actor', 'subscribe_actor', 'build_actor']

# --------------------
# Module Attributes
# --------------------

__actorscontr__ = {}


# --------------------
# Module classes
# --------------------


class Actor(ABC):
    """An actor is an asynchronous delegate that monitors a process and handles messaging between components"""
    __slots__ = ('__actorname__', '__mq__', '__managerq__', '__lastchange__', '__sleep__')

    def __init__(self,
                 name: str,
                 mq: multiprocessing.Queue,
                 managerq: multiprocessing.Queue,
                 sleep: int,
                 *args, **kwargs):
        if not name:
            raise IllegalValueException("Can't create an unnamed actor")
        self.__actorname__ = name
        self.__mq__ = mq
        self.__managerq__ = managerq
        self.__sleep__ = sleep

    @property
    def name(self):
        return self.__actorname__

    @name.setter
    def name(self, value: str):
        self.__actorname__ = value

    def __poll(self) -> Union[Signal, None]:
        try:
            msg = self.__mq__.get_nowait()
            return self._handlemessage(msg)
        except Empty:
            return None

    def _handlemessage(self, msg: Message) -> Union[Signal, None]:
        msgsig = msg.header['Signal']
        if msgsig is Signal.BEAT:
            return self._handlebeat(msg)
        elif msgsig is Signal.DESTROY:
            return self._handledestroy(msg)
        elif msgsig is Signal.KILL:
            return self._handlekill(msg)
        else:
            return None

    def _sendmessage(self, msgsignal: Signal, msgtype: MsgType, msgbody):
        msgbuilder = MessageFactory(self.name)
        msgbuilder.signal = msgsignal
        msgbuilder.type = msgtype
        if msgbody:
            msgbuilder.body = msgbody
        self.__managerq__.put_nowait(msgbuilder.build())

    # noinspection PyMethodMayBeStatic
    def _handledestroy(self, msg: Message) -> Union[Signal, None]:
        return Signal.DESTROY

    @abstractmethod
    def _handlekill(self, msg: Message) -> Union[Signal, None]:
        pass

    @abstractmethod
    def _resolvestatus(self) -> str:
        pass

    def _handlebeat(self, msg: Message) -> Union[Signal, None]:
        """Handles a BEAT signal coming from the queue"""
        # Un BEAT può avere due payload: uno STATUS e un NONE
        # STATUS richiede una risposta completa, NONE si accountenta di un messaggio in ritorno
        beattype = msg.header['Type']
        if beattype is MsgType.NONE:
            self._sendmessage(Signal.BEAT, MsgType.NONE, None)
        elif beattype is MsgType.STATUS:
            beatbody = msg.body
            respbody = {'reqtime': beatbody['reqtime'],
                        'status': self._resolvestatus(),
                        'beattime': datetime.now(),
                        'statustime': self.__lastchange__,
                        'statusmessage': None}
            self._sendmessage(Signal.BEAT, MsgType.STATUS, respbody)
        return Signal.BEAT

    @abstractmethod
    def _scheduleexec(self):
        pass

    def run(self):
        while 1:
            # sleep
            for i in range(self.__sleep__):
                sig = self.__poll()
                if sig is Signal.DESTROY:
                    return
                time.sleep(1)

            self._scheduleexec()


# --------------------
# Module Functions
# --------------------


def subscribe_actor(actorname: str, factorycall: Callable):
    __actorscontr__[actorname] = factorycall


def build_actor(actorname: str, *args, **kwargs):
    factorycall = __actorscontr__[actorname]
    factorycall(*args, **kwargs)

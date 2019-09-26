import multiprocessing
import time
from abc import ABC, abstractmethod
from concurrent.futures.thread import ThreadPoolExecutor
from datetime import datetime
from queue import Full, Empty
from typing import Union

import attr

from theater.core.components.constants import INTERRUPTED_STATUS, IDLE_STATUS, MSGHANDLING_STATUS
from theater.core.constants import Signal, MsgType
from theater.core.errors import IllegalValueException, ScoreEnd
from theater.core.messages import Message, Status

__all__ = ['BaseComponent', 'BaseMusician', 'DelegatingMusician']


class BaseComponent(ABC):
    """A component handles the execution of a recurring task that accepts external input in the form of Messages"""
    __slots__ = ('__actorname', '__mq', '__pausetime')

    # --------------------
    # BaseComponent Constructor
    # --------------------

    def __init__(self,
                 name: str,
                 mpq: multiprocessing.Queue,
                 pausetime: int,
                 *args, **kwargs):
        """
        Builds the essential skeleton for a Component
        :param name: The name assigned to this component. A None name raises an IllegalValueException
        :param mpq: The multiprocessing.Queue from which the component receives messages
        :param pausetime: The number of ticks in which the component sleeps while polling the internal queue. 1 tick
        should be very close to 1 second
        """
        if not name:
            raise IllegalValueException("Can't create an unnamed actor")
        self.__actorname = name
        self.__mq = mpq
        self.__pausetime = pausetime

    # --------------------
    # BaseComponent protected properties
    # --------------------

    @property
    def _actorname(self):
        return self.__actorname

    @property
    def _mq(self):
        return self.__mq

    @property
    def _pausetime(self):
        return self.__pausetime

    # --------------------
    # BaseComponent public methods
    # --------------------

    def run(self):
        """Pauses and executes custom code in an endless cycle, till an Exception interrupts it"""
        while 1:
            self._pause()
            self._onpauseend()

    # --------------------
    # BaseComponent protected methods
    # --------------------

    def _handlemessage(self, msg: Message) -> Union[Signal, None]:
        """Reads a Signal in a message, than redirects the handling to a specialized method. Returns a Signal or None"""
        msgsignal = msg.signal
        if msgsignal is Signal.BEAT:
            return self._handlebeat(msg)
        elif msgsignal is Signal.TRIGGER:
            return self._handletrigger(msg)
        elif msgsignal is Signal.UPDATE:
            return self._handleupdate(msg)
        elif msgsignal is Signal.INTERRUPT:
            return self._handleinterrupt(msg)
        elif msgsignal is Signal.CREATE:
            return self._handlecreate(msg)
        elif msgsignal is Signal.KILL:
            return self._handlekill(msg)
        else:
            return None

    def _handlebeat(self, _: Message) -> Union[Signal, None]:
        return Signal.BEAT

    def _handletrigger(self, _: Message) -> Union[Signal, None]:
        return Signal.TRIGGER

    def _handleupdate(self, _: Message) -> Union[Signal, None]:
        return Signal.UPDATE

    def _handleinterrupt(self, _: Message) -> Union[Signal, None]:
        return Signal.INTERRUPT

    def _handlecreate(self, _: Message) -> Union[Signal, None]:
        return Signal.CREATE

    def _handlekill(self, _: Message) -> Union[Signal, None]:
        return Signal.KILL

    def _interrupthook(self):
        """Executes code right before an interruption caused by a Signal INTERRUPT returned by _handlemessage"""
        pass

    @abstractmethod
    def _onpauseend(self, *args, **kwargs):
        """Does something after the pause period, than gets scheduled again"""
        pass

    # --------------------
    # BaseComponent private methods
    # --------------------

    def _poll(self) -> Union[Signal, None]:
        """Polls the internal queue. If a message is found, it's handled. It returns a Signal on a succesful
        message handling, or None if nothing have been processed/something went wrong"""
        try:
            msg = self._mq.get_nowait()
            return self._handlemessage(msg)
        except Empty:
            return None

    def _pause(self):
        """The components polls the internal queue, than sleeps for 1 second. This happens for _pausetime ticks"""
        for i in range(self._pausetime):
            sig = self._poll()
            if sig is Signal.INTERRUPT:
                self._interrupthook()
                raise ScoreEnd("Interrupted by INTERRUPT Message")
            time.sleep(1)


class BaseMusician(BaseComponent, ABC):
    """A Musician is a "Conducted" component, meaning that he's able to send messages of it's own to it's manager.
    It stores the time of its creation for detailed heartbeats"""
    __slots__ = ('__conductorsq', '__starttime')

    # --------------------
    # BaseMusician constructor
    # --------------------

    def __init__(self,
                 name: str,
                 mpq: multiprocessing.Queue,
                 pausetime: int,
                 conductorq: multiprocessing.Queue,
                 *args, **kwargs):
        """
        extends theather.core.components.abc.BaseComponent
        :param conductorq: The queue used by the Musician to send messages
        """
        super().__init__(name, mpq, pausetime, *args, **kwargs)
        self.__conductorsq = conductorq
        self.__starttime = datetime.now()

    # --------------------
    # BaseMusician protected properties
    # --------------------

    @property
    def _conductorsq(self):
        return self.__conductorsq

    @property
    def _starttime(self):
        return self.__starttime

    # --------------------
    # BaseMusician protected methods
    # --------------------

    def _handlebeat(self, msg: Message) -> Union[Signal, None]:
        """It sends a BEAT message using the _conductorq if the message body is NONE or STATUS. The answer
        depends on the body type of the incoming message"""
        msgtype = msg.type
        if msgtype is MsgType.NONE:
            self._answerconductor(Signal.BEAT, MsgType.NONE, None)
            return Signal.BEAT
        elif msgtype is MsgType.STATUS:
            newbody = attr.evolve(msg.body,
                                  status="Running", time=datetime.now(),
                                  statustime=self._starttime, statusmessage=None)
            self._answerconductor(Signal.BEAT, MsgType.STATUS, newbody)
            return Signal.BEAT
        else:
            return None

    def _catchsendexception(self, exc: Exception):
        pass

    def _interrupthook(self):
        """Sends a detailed BEAT message, indicating that this Musician has been interrupted"""
        self._answerconductor(Signal.BEAT, MsgType.STATUS, Status(reqtime=None,
                                                                  status=INTERRUPTED_STATUS,
                                                                  time=datetime.now(),
                                                                  statustime=datetime.now(),
                                                                  statusmessage="End of actors execution"))

    def _answerconductor(self, msgsignal: Signal, msgtype: MsgType, msgbody):
        """Handles creation and shipping of a message toward the Musician's _conductorsq"""
        msg = Message(sender=self.__actorname,
                      signal=msgsignal,
                      type=msgtype,
                      body=msgbody)
        try:
            self._conductorsq.put_nowait(msg)
        except Full as e:
            self._catchsendexception(e)


class DelegatingMusician(BaseMusician, ABC):
    """A Musician that delegates his execution logic to a thread of its own. Since it's 'free' while executing
    he's able to handle messages in every moment and it can also kill tasks. Also he retains a customized status,
    an - optional - description of it and the time in which the status changed"""
    __slots__ = ('__status', '__statusdetail', '__statustime')

    # --------------------
    # DelegatingMusician Constructor
    # --------------------

    def __init__(self,
                 name: str,
                 mpq: multiprocessing.Queue,
                 pausetime: int,
                 conductorq: multiprocessing.Queue,
                 *args,
                 **kwargs):
        """
        extends theather.core.components.abc.BaseMusician
        """
        super().__init__(name, mpq, pausetime, conductorq, *args, **kwargs)
        self.__status = None
        self.__statusdetail = None
        self.__statustime = None

    # --------------------
    # DelegatingMusician protected properties
    # --------------------

    @property
    def _status(self) -> str:
        return self.__status

    @_status.setter
    def _status(self, value: str):
        self.__status = value

    @property
    def _statusdetail(self) -> Union[str, None]:
        return self.__statusdetail

    @_statusdetail.setter
    def _statusdetail(self, value: Union[str, None]):
        self.__statusdetail = value

    @property
    def _statustime(self) -> datetime:
        return self.__statustime

    @_statustime.setter
    def _statustime(self, _: datetime):
        self.__statustime = datetime.now()

    # --------------------
    # DelegatingMusician public methods
    # --------------------

    def run(self):
        with ThreadPoolExecutor(max_workers=1) as executor:
            while 1:
                # Status reset
                self._status = IDLE_STATUS
                self._statusdetail = f"Running since {super()._starttime}"
                self._statustime = datetime.now()
                # Execution
                self._pause()
                self._onpauseend(executor=executor)

    # --------------------
    # DelegatingMusician protected methods
    # --------------------

    def _handlebeat(self, msg: Message) -> Union[Signal, None]:
        """extends BaseMusician._handlebeat. It adds the status states to the STATUS beat"""
        msgtype = msg.type
        if msgtype is MsgType.NONE:
            self._answerconductor(Signal.BEAT, MsgType.NONE, None)
            return Signal.BEAT
        elif msgtype is MsgType.STATUS:
            self._answerconductor(Signal.BEAT, MsgType.STATUS, Status(reqtime=None,
                                                                      status=self._status,
                                                                      time=datetime.now(),
                                                                      statustime=self._statustime,
                                                                      statusmessage=self._statusdetail))
            return Signal.BEAT
        else:
            return None

    def _poll(self) -> Union[Signal, None]:
        """extends BaseComponent._poll. It adds status handling to its process"""
        try:
            msg = self._mq.get_nowait()
            self._status = MSGHANDLING_STATUS
            self._statustime = datetime.now()
            return self._handlemessage(msg)
        except Empty:
            return None
        finally:
            if self._status is not IDLE_STATUS:
                self._status = IDLE_STATUS
                self._statusdetail = f"Running since {super()._starttime}"
                self._statustime = datetime.now()

    @abstractmethod
    def _onpauseend(self, executor=None, *args, **kwargs):
        pass

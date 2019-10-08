# -*- coding: utf-8 -*-
import multiprocessing
import queue
import typing
from collections import OrderedDict
from datetime import datetime
from typing import Optional

import attr

from theater.conductor.constants import MONITOR
from theater.conductor.structures import ManagedComponent
from theater.core.components.abc import BaseMusician, StateAware
from theater.core.components.constants import IDLE_STATUS
from theater.core.constants import Signal, MsgType
from theater.core.errors import IllegalValueException, IllegalActionException
from theater.core.messages import generatequeues, Message


class BaseConductor(BaseMusician, StateAware):
    """ """
    __slots__ = ('__musicians', '__stage', '__status', '__statustime', '__statusdetail')

    # --------------------
    # BaseConductor Constructor
    # --------------------

    def __init__(self,
                 name: str,
                 pausetime: int,
                 *args, **kwargs):
        outboxqueue, inboxqueue = generatequeues()
        super().__init__(name, outboxqueue, pausetime, inboxqueue, *args, **kwargs)
        self.__stage: typing.Dict[str, ManagedComponent] = OrderedDict()
        self.__musicians: typing.Dict[str, str] = OrderedDict()
        self.__status = IDLE_STATUS
        self.__statustime = datetime.now()
        self.__statusdetail = None

    # --------------------
    # BaseConductor protected properties
    # --------------------

    @property
    def _status(self):
        return self.__status

    @property
    def _statustime(self):
        return self.__statustime

    @property
    def _statusdetail(self):
        return self.__statusdetail

    # --------------------
    # BaseConductor protected methods
    # --------------------

    def _updatestatus(self, pstatus: str, pdetail: Optional[str]) -> None:
        if not pstatus:
            raise IllegalValueException()
        self.__status = pstatus
        self.__statustime = datetime.now()
        self.__statusdetail = pdetail

    def _answerconductor(self, msgsignal: Signal, msgtype: MsgType, msgbody):
        pass

    def _resolvecomponentname(self, childuuid) -> Optional[str]:
        return self.__musicians.get(childuuid)

    def _resolvecomponentuuid(self, childname) -> Optional[str]:
        component = self.__stage.get(childname)
        if component:
            return component.uuid
        else:
            return None

    def _getcomponent(self, childname) -> Optional[ManagedComponent]:
        return self.__stage.get(childname)

    def _components(self):
        for item in self.__stage.values():
            yield item

    def _touchcomponent(self, childname):
        component = self.__stage.get(childname)
        if not component:
            raise IllegalActionException()
        component = attr.evolve(component, beattime=datetime.now())
        self.__stage[childname] = component

    def _registercomponent(self, childuuid, childname, childproc, childq) -> bool:
        # FIXME Implementa
        pass

    def _unregistercomponent(self, childname) -> bool:
        # FIXME Implementa
        pass

    def _cleanuuid(self, rogueuuid) -> bool:
        # FIXME Implementa
        pass

    def _createcomponent(self, compname, compconf) \
            -> typing.Tuple[str, str, multiprocessing.Process, multiprocessing.Queue]:
        # FIXME Implementa
        pass

    def _handlebeat(self, msg: Message) -> typing.Optional[Signal]:
        sendername = self._resolvecomponentname(msg.sender)
        if not sendername:
            return None
        if msg.type is MsgType.STATUS:
            if sendername is MONITOR:
                self._touchcomponent(MONITOR)
                # Monitor wants heartbeats for every registered component
                for component in self._components():
                    if component.name is MONITOR:
                        pbody = attr.evolve(msg.body, status=self._status, time=datetime.now(),
                                            statustime=self._statustime, statusmessage=self._statusdetail)
                        pmsg = attr.evolve(msg, body=pbody, sender=self._actorname)
                        try:
                            component.queue.put_nowait(pmsg)
                        except queue.Full as e:
                            self._catchsendexception(e)
                    else:
                        pmsg = attr.evolve(msg, sender=MONITOR)
                        try:
                            component.queue.put_nowait(pmsg)
                        except queue.Full as e:
                            self._catchsendexception(e)
                return Signal.BEAT
            else:
                self._touchcomponent(sendername)
                pmsg = attr.evolve(msg, sender=sendername)
                try:
                    self._getcomponent(MONITOR).queue.put_nowait(pmsg)
                except queue.Full as e:
                    self._catchsendexception(e)
                return Signal.BEAT
        elif msg.type is MsgType.NONE:
            self._touchcomponent(sendername)
        else:
            return None

    def _onpauseend(self, *args, **kwargs):
        pass

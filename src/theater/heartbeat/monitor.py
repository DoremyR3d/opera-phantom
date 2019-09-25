import multiprocessing
from datetime import datetime
from typing import Union

from . import HB_REQTIME, HB_STATUS, HB_STATUSMESSAGE, HB_STATUSTIME, HB_TIME

from theater import Actor
from theater import subscribe_actor
from theater import Message, Signal, MsgType
from theater import SENDER_KEY, MSGTYPE_KEY
from theater import Loggable

__all__ = []


# --------------------
# Module classes
# --------------------


class Monitor(Actor, Loggable):
    __slots__ = ('__action__', '__status__', '__datestart__')

    def __init__(self,
                 name: str,
                 mq: multiprocessing.Queue,
                 managerq: multiprocessing.Queue,
                 sleep: int,
                 configuration: dict,
                 *args, **kwargs):
        super().__init__(name, mq, managerq, sleep, *args, **kwargs)
        self.init_logger(configuration)
        self.__datestart__ = datetime.now()

        def monitor():
            self._sendmessage(Signal.BEAT,
                              MsgType.STATUS,
                              {HB_REQTIME: datetime.now(),
                               HB_STATUS: None,
                               HB_TIME: None,
                               HB_STATUSTIME: None,
                               HB_STATUSMESSAGE: None})
            # Non stampa i tempi di richiesta visto che avviene tutto qui
            self.info(f"{self.name}[RUNNING since {self.__datestart__}]")

        self.__action__ = monitor

    def _handlekill(self, msg: Message) -> Union[Signal, None]:
        # Nulla da uccidere, visto che questo actor si limita a mandare un messaggio
        self.debug("Received a KILL signal ", msg)
        return None

    def _handlebeat(self, msg: Message) -> Union[Signal, None]:
        # Qui la gestione cambia, perché sto gestendo un monitor.
        beattype = msg.header[MSGTYPE_KEY]
        if beattype is MsgType.NONE:
            # Qui gestisco il mio beat, visto che il manager vuole sapere se sono in esecuzione
            self.info(f"{self.name}[RUNNING since {self.__datestart__}]")
            self._sendmessage(Signal.BEAT, MsgType.NONE, None)
        elif beattype is MsgType.STATUS:
            # Qui gestisco il beat di un altro Actor
            beatbody = msg.body
            self.info(f"{msg.header[SENDER_KEY]}[{beatbody['status']} since {beatbody['statustime']}]" +
                      f"[Requested: {beatbody['reqtime']}, Answered: {beatbody['beattime']}]: {beatbody.statusmessage}")
        return Signal.BEAT

    def _scheduleexec(self):
        # Visto che deve solo eseguire compiti banali non gestisco sleep, messaggi o timeouts
        self.__action__()

    def _resolvestatus(self) -> str:
        # Esiste un solo stato
        return "RUNNING"


# --------------------
# Module Functions
# --------------------


def monitorfactory(*args, **kwargs):
    return Monitor(*args, **kwargs)


# --------------------
# Module init
# --------------------


subscribe_actor("SimpleMonitor", monitorfactory)

import enum
from typing import NamedTuple, Any

from theater.act.errors import IllegalActionException, IllegalValueException

__all__ = ['Signal', 'MsgType', 'Message', 'SENDER_KEY', 'SIGNAL_KEY', 'MSGTYPE_KEY']

# --------------------
# Module Attributes
# --------------------

SENDER_KEY: str = 'Sender'
SIGNAL_KEY: str = 'Signal'
MSGTYPE_KEY: str = 'MsgType'


# --------------------
# Module Classes
# --------------------


class Signal(enum.Enum):
    """Enum that contains all possibile signals stored in a Message's header"""
    CREATE = 'CREATE'
    DESTROY = 'DESTROY'
    BEAT = 'BEAT'
    KILL = 'KILL'


class MsgType(enum.Enum):
    """Enum that contains all possibile type for a Message's body"""
    NONE = "None"
    TEXT = "Text"
    MAP = "Map"
    STATUS = "Status"
    BYTES = "Bytes"


class Message:
    """Type class for Messages"""
    __slots__ = ('header', 'body')

    def __init__(self):
        raise IllegalActionException("You can't create a Message outside of a MessageFactory!")


class ActorMessage(NamedTuple, Message):
    """Messages exchanged between act"""
    header: dict
    body: Any


class MessageFactory:
    """Builder for messages"""
    __slots__ = ('__sender__', '__signal__', '__type__', '__body__', '__header__')

    def __init__(self, sender):
        self.__sender__ = sender if isinstance(sender, str) else sender.name
        self.__signal__ = None
        self.__type__ = None
        self.__body__ = None
        self.__header__ = {}

    @property
    def type(self):
        return self.__type__

    @type.setter
    def type(self, newtype: MsgType):
        self.__type__ = newtype

    @property
    def signal(self):
        return self.__signal__

    @signal.setter
    def signal(self, newsignal: Signal):
        self.__signal__ = newsignal

    def extend_header(self, key: str, value):
        self.__header__[key] = value

    @property
    def body(self):
        return self.__body__

    @body.setter
    def body(self, newbody):
        if self.__type__ is None:
            raise IllegalActionException("You can't add a body without first specifying its type!")
        elif self.__type__ is MsgType.TEXT:
            if not isinstance(newbody, str):
                raise IllegalValueException("A type TEXT requires a str body")
        elif self.__type__ is MsgType.STATUS:
            if not isinstance(newbody, dict):
                raise IllegalValueException("A type STATUS requires a dict body")
            # FIXME Estendi il controllo
        elif self.__type__ is MsgType.BYTES:
            if not isinstance(newbody, bytes):
                raise IllegalValueException("A type BYTES requires a bytes body")
        elif self.__type__ is MsgType.MAP:
            if not isinstance(newbody, dict):
                raise IllegalValueException("A type MAP requires a dict body")
        elif self.__type__ is MsgType.NONE:
            if newbody:
                raise IllegalValueException("A type NONE requires a None body")
        else:
            raise IllegalValueException("This factory doesn't support adding a body for this type of message")
        self.__body__ = newbody

    def build(self):
        if not self.__sender__:
            raise IllegalActionException("Can't create a message without info about its sender")
        if not self.__type__:
            raise IllegalActionException("Can't create a message without info about its type")
        if not self.__signal__:
            raise IllegalActionException("Can't create a message without a signal to send")
        self.__header__[SENDER_KEY] = self.__sender__
        self.__header__[MSGTYPE_KEY] = self.__type__
        self.__header__[SIGNAL_KEY] = self.__signal__
        return ActorMessage(header=self.__header__, body=self.__body__)

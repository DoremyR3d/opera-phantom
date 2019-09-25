from typing import NamedTuple, Any

from theater.core.constants import Signal, MsgType, SENDER_KEY, MSGTYPE_KEY, SIGNAL_KEY, \
    HB_REQTIME, HB_STATUS, HB_TIME, HB_STATUSTIME, HB_STATUSMESSAGE
from theater.core.errors import IllegalActionException, IllegalValueException

__all__ = ['Message', 'MessageFactory']


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
    __slots__ = ('__sender', '__signal', '__type', '__body', '__header')

    def __init__(self, sender):
        self.__sender = sender if isinstance(sender, str) else sender.name
        self.__signal = None
        self.__type = None
        self.__body = None
        self.__header = {}

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, newtype: MsgType):
        self.__type = newtype

    @property
    def signal(self):
        return self.__signal

    @signal.setter
    def signal(self, newsignal: Signal):
        self.__signal = newsignal

    def extend_header(self, key: str, value):
        self.__header[key] = value

    @property
    def body(self):
        return self.__body

    @body.setter
    def body(self, newbody):
        if self.__type is None:
            raise IllegalActionException("You can't add a body without first specifying its type!")
        elif self.__type is MsgType.TEXT:
            if not isinstance(newbody, str):
                raise IllegalValueException("A type TEXT requires a str body")
        elif self.__type is MsgType.STATUS:
            if not isinstance(newbody, dict):
                raise IllegalValueException("A type STATUS requires a dict body")
            try:
                _ = newbody[HB_REQTIME]
                _ = newbody[HB_STATUS]
                _ = newbody[HB_TIME]
                _ = newbody[HB_STATUSTIME]
                _ = newbody[HB_STATUSMESSAGE]
            except KeyError:
                raise IllegalValueException("A body of type STATUS is required to contain all the requested keys")
            # FIXME Estendi il controllo
        elif self.__type is MsgType.BYTES:
            if not isinstance(newbody, bytes):
                raise IllegalValueException("A type BYTES requires a bytes body")
        elif self.__type is MsgType.MAP:
            if not isinstance(newbody, dict):
                raise IllegalValueException("A type MAP requires a dict body")
        elif self.__type is MsgType.NONE:
            if newbody:
                raise IllegalValueException("A type NONE requires a None body")
        else:
            raise IllegalValueException("This factory doesn't support adding a body for this type of message")
        self.__body = newbody

    def build(self):
        if not self.__sender:
            raise IllegalActionException("Can't create a message without info about its sender")
        if not self.__type:
            raise IllegalActionException("Can't create a message without info about its type")
        if not self.__signal:
            raise IllegalActionException("Can't create a message without a signal to send")
        self.__header[SENDER_KEY] = self.__sender
        self.__header[MSGTYPE_KEY] = self.__type
        self.__header[SIGNAL_KEY] = self.__signal
        return ActorMessage(header=self.__header, body=self.__body)

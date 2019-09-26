from datetime import datetime
from typing import Optional

import attr

from theater.core.constants import Signal, MsgType
from theater.core.errors import IllegalActionException, IllegalValueException

__all__ = ['Message', 'Status']


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

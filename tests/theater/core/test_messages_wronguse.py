# -*- coding: utf-8 -*-
from datetime import datetime

import pytest

from theater.core.constants import MsgType, Signal, HB_REQTIME, HB_STATUSMESSAGE, HB_STATUS, HB_STATUSTIME, HB_TIME
from theater.core.errors import IllegalActionException, IllegalValueException
from theater.core.messages import MessageFactory


class TestMessageFactoryWrongUse:
    def test_bodybeforehead(self):
        with pytest.raises(IllegalActionException):
            msgfact = MessageFactory("TestSender")
            msgfact.body = None
            msgfact.type = MsgType.NONE
            msgfact.signal = Signal.BEAT
            _ = msgfact.build()

    def test_nosignal(self):
        with pytest.raises(IllegalActionException):
            msgfact = MessageFactory("TestSender")
            msgfact.type = MsgType.NONE
            msgfact.body = None
            _ = msgfact.build()

    def test_notype(self):
        with pytest.raises(IllegalActionException):
            msgfact = MessageFactory("TestSender")
            msgfact.signal = Signal.BEAT
            _ = msgfact.build()

    def test_nosender(self):
        with pytest.raises(IllegalActionException):
            msgfact = MessageFactory(None)
            msgfact.signal = Signal.BEAT
            msgfact.type = MsgType.TEXT
            msgfact.body = "I shouldn't be here"
            _ = msgfact.build()

    def test_illegalsender(self):
        with pytest.raises(IllegalActionException):
            class Dummy(object):
                @property
                def name(self):
                    return "ACABDummy"

            msgfact = MessageFactory(Dummy())
            msgfact.type = MsgType.TEXT
            msgfact.signal = Signal.TRIGGER
            msgfact.body = "ACAB"
            _ = msgfact.build()

    def test_nonemismatch(self):
        with pytest.raises(IllegalValueException):
            msgfact = MessageFactory("TestSender")
            msgfact.type = MsgType.NONE
            msgfact.signal = Signal.TRIGGER
            msgfact.body = "ACAB"
            _ = msgfact.build()

    def test_textmismatch(self):
        with pytest.raises(IllegalValueException):
            msgfact = MessageFactory("TestSender")
            msgfact.type = MsgType.TEXT
            msgfact.signal = Signal.TRIGGER
            msgfact.body = 42
            _ = msgfact.build()

    def test_bytesmismatch(self):
        with pytest.raises(IllegalValueException):
            msgfact = MessageFactory("TestSender")
            msgfact.type = MsgType.BYTES
            msgfact.signal = Signal.TRIGGER
            msgfact.body = "ACAB"
            _ = msgfact.build()

    def test_mapmismatch(self):
        with pytest.raises(IllegalValueException):
            msgfact = MessageFactory("TestSender")
            msgfact.type = MsgType.MAP
            msgfact.signal = Signal.TRIGGER
            msgfact.body = "ACAB"
            _ = msgfact.build()

    def test_statusmismatch(self):
        with pytest.raises(IllegalValueException):
            msgfact = MessageFactory("TestSender")
            msgfact.type = MsgType.STATUS
            msgfact.signal = Signal.TRIGGER
            msgfact.body = "ACAB"
            _ = msgfact.build()

    def test_illegalstatus(self):
        with pytest.raises(IllegalValueException):
            msgfact = MessageFactory("TestSender")
            msgfact.type = MsgType.STATUS
            msgfact.signal = Signal.BEAT
            msgfact.body = {"ACAB": "YOLO"}
            _ = msgfact.build()

    def test_partialstatus(self):
        with pytest.raises(IllegalValueException):
            msgfact = MessageFactory("TestSender")
            msgfact.type = MsgType.STATUS
            msgfact.signal = Signal.BEAT
            msgfact.body = {HB_REQTIME: datetime.now()}
            _ = msgfact.build()

    def test_statuswrongtypes(self):
        msgfact = MessageFactory("TestSender")
        msgfact.type = MsgType.STATUS
        msgfact.signal = Signal.BEAT
        with pytest.raises(IllegalValueException):
            msgfact.body = {
                HB_REQTIME: "Now",
                HB_STATUSMESSAGE: "Test",
                HB_STATUS: "Test",
                HB_STATUSTIME: datetime.now(),
                HB_TIME: datetime.now()
            }
        with pytest.raises(IllegalValueException):
            msgfact.body = {
                HB_REQTIME: datetime.now(),
                HB_STATUSMESSAGE: 5,
                HB_STATUS: "Test",
                HB_STATUSTIME: datetime.now(),
                HB_TIME: datetime.now()
            }
        with pytest.raises(IllegalValueException):
            msgfact.body = {
                HB_REQTIME: datetime.now(),
                HB_STATUSMESSAGE: "Test",
                HB_STATUS: 5,
                HB_STATUSTIME: datetime.now(),
                HB_TIME: datetime.now()
            }
        with pytest.raises(IllegalValueException):
            msgfact.body = {
                HB_REQTIME: datetime.now(),
                HB_STATUSMESSAGE: "Test",
                HB_STATUS: "Test",
                HB_STATUSTIME: "Now",
                HB_TIME: datetime.now()
            }
        with pytest.raises(IllegalValueException):
            msgfact.body = {
                HB_REQTIME: datetime.now(),
                HB_STATUSMESSAGE: "Test",
                HB_STATUS: "Test",
                HB_STATUSTIME: datetime.now(),
                HB_TIME: "Now"
            }

    pass

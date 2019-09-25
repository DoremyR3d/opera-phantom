# -*- coding: utf-8 -*-
from datetime import datetime

from theater.core.constants import MsgType, SENDER_KEY, MSGTYPE_KEY, SIGNAL_KEY, HB_REQTIME, HB_STATUS, HB_TIME, \
    HB_STATUSTIME, HB_STATUSMESSAGE
from theater.core.constants import Signal
from theater.core.messages import MessageFactory


class TestMessageFactory:
    def __initfact(self) -> MessageFactory:
        testfact = MessageFactory("Test")
        assert testfact

        testfact.signal = Signal.BEAT
        return testfact

    def test_msgtypenone(self):
        testfact = self.__initfact()
        testfact.type = MsgType.NONE
        testfact.body = None
        out = testfact.build()

        assert out.header == {SENDER_KEY: "Test", MSGTYPE_KEY: MsgType.NONE, SIGNAL_KEY: Signal.BEAT}
        assert out.body is None

    def test_msgtypetext(self):
        testfact = self.__initfact()
        testfact.type = MsgType.TEXT
        testfact.body = "Test body"
        out = testfact.build()

        assert out.header == {SENDER_KEY: "Test", MSGTYPE_KEY: MsgType.TEXT, SIGNAL_KEY: Signal.BEAT}
        assert out.body == "Test body"

    def test_msgtypestatus(self):
        testfact = self.__initfact()
        testfact.type = MsgType.STATUS
        dtnow = datetime.now()
        testfact.body = {
            HB_REQTIME: dtnow,
            HB_STATUS: "Test",
            HB_TIME: dtnow,
            HB_STATUSTIME: dtnow,
            HB_STATUSMESSAGE: "Test status"
        }
        out = testfact.build()

        assert out.header == {SENDER_KEY: "Test", MSGTYPE_KEY: MsgType.STATUS, SIGNAL_KEY: Signal.BEAT}
        assert out.body == {HB_REQTIME: dtnow, HB_STATUS: "Test", HB_TIME: dtnow, HB_STATUSTIME: dtnow,
                            HB_STATUSMESSAGE: "Test status"}

    def test_msgtypebytes(self):
        testfact = self.__initfact()
        testfact.type = MsgType.BYTES
        testfact.body = b'Test message'
        out = testfact.build()

        assert out.header == {SENDER_KEY: "Test", MSGTYPE_KEY: MsgType.BYTES, SIGNAL_KEY: Signal.BEAT}
        assert out.body == b'Test message'

    def test_msgtypemap(self):
        testfact = self.__initfact()
        testfact.type = MsgType.MAP
        testfact.body = {'Test': 'Map'}
        out = testfact.build()

        assert out.header == {SENDER_KEY: "Test", MSGTYPE_KEY: MsgType.MAP, SIGNAL_KEY: Signal.BEAT}
        assert out.body == {"Test": "Map"}

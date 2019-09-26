# -*- coding: utf-8 -*-
from datetime import datetime

import pytest

from theater.core.constants import MsgType, Signal
from theater.core.messages import Message, Status


class TestMessageWrongUsage:
    def test_nosignal(self):
        with pytest.raises(TypeError):
            _ = Message(sender="TestSender", type=MsgType.NONE, body=None)

    def test_nonesignal(self):
        with pytest.raises(TypeError):
            _ = Message(sender="TestSender", type=MsgType.NONE, signal=None, body=None)

    def test_notype(self):
        with pytest.raises(TypeError):
            _ = Message(sender="TestSender", signal=Signal.TRIGGER, body=None)

    def test_nonetype(self):
        with pytest.raises(TypeError):
            _ = Message(sender="TestSender", signal=Signal.TRIGGER, type=None, body=None)

    def test_nosender(self):
        with pytest.raises(TypeError):
            _ = Message(signal=Signal.TRIGGER, type=MsgType.NONE, body=None)

    def test_nonesender(self):
        with pytest.raises(TypeError):
            _ = Message(sender=None, signal=Signal.TRIGGER, type=MsgType.NONE, body=None)

    def test_nonemismatch(self):
        with pytest.raises(TypeError):
            _ = Message(sender="TestSender", type=MsgType.NONE, signal=Signal.TRIGGER, body="ACAB")

    def test_textmismatch(self):
        with pytest.raises(TypeError):
            _ = Message(sender="TestSender", type=MsgType.TEXT, signal=Signal.TRIGGER, body=42)

    def test_bytesmismatch(self):
        with pytest.raises(TypeError):
            _ = Message(sender="TestSender", type=MsgType.BYTES, signal=Signal.TRIGGER, body="ACAB")

    def test_mapmismatch(self):
        with pytest.raises(TypeError):
            _ = Message(sender="TestSender", type=MsgType.MAP, signal=Signal.TRIGGER, body="ACAB")

    def test_statusmismatch(self):
        with pytest.raises(TypeError):
            _ = Message(sender="TestSender", type=MsgType.STATUS, signal=Signal.TRIGGER, body="ACAB")

    def test_partialstatus(self):
        with pytest.raises(TypeError):
            tsstat = Status(reqtime=datetime.now())
            _ = Message(sender="TestSender", type=MsgType.STATUS, signal=Signal.BEAT, body=tsstat)


class TestStatusWrongUsage:
    def test_wrongreqtimetype(self):
        with pytest.raises(TypeError):
            _ = Status(reqtime="Now", statusmessage="Test", status="Test",
                       statustime=datetime.now(), time=datetime.now())

    def test_wrongstatusmessagetype(self):
        with pytest.raises(TypeError):
            _ = Status(reqtime=datetime.now(), statusmessage=5, status="Test",
                       statustime=datetime.now(), time=datetime.now())

    def test_wrongstatustype(self):
        with pytest.raises(TypeError):
            _ = Status(reqtime=datetime.now(), statusmessage="Test", status=5,
                       statustime=datetime.now(), time=datetime.now())

    def test_wrongstatustimetype(self):
        with pytest.raises(TypeError):
            _ = Status(reqtime=datetime.now(), statusmessage="Test", status="Test",
                       statustime="Now", time=datetime.now())

    def test_wrongtimetype(self):
        with pytest.raises(TypeError):
            _ = Status(reqtime=datetime.now(), statusmessage="Test", status="Test",
                       statustime=datetime.now(), time="Now")

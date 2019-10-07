# -*- coding: utf-8 -*-
import multiprocessing
import queue
from datetime import datetime

import pytest

from theater.core.constants import MsgType, Signal
from theater.core.errors import IllegalActionException
from theater.core.messages import Message, Status, ConsumerQueue, ProducerQueue


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


class TestProducer:
    def test_randomq(self):
        randomq = queue.Queue()
        with pytest.raises(TypeError):
            _ = ProducerQueue(randomq)

    def test_get(self):
        testq = multiprocessing.Queue()
        producer = ProducerQueue(testq)
        with pytest.raises(IllegalActionException):
            producer.get_nowait()
        with pytest.raises(IllegalActionException):
            producer.get(False)


class TestConsumer:
    def test_randomq(self):
        randomq = queue.Queue()
        with pytest.raises(TypeError):
            _ = ConsumerQueue(randomq)

    def test_put(self):
        testq = multiprocessing.Queue()
        consumer = ConsumerQueue(testq)
        with pytest.raises(IllegalActionException):
            consumer.put_nowait("_")
        with pytest.raises(IllegalActionException):
            consumer.put("_", False)

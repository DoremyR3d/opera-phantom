# -*- coding: utf-8 -*-
import multiprocessing
from datetime import datetime

import pytest
from _queue import Empty

from theater.core.constants import MsgType
from theater.core.constants import Signal
from theater.core.messages import Message, Status, ProducerQueue, ConsumerQueue, generatequeues


class TestMessage:
    def test_msgtypenone(self):
        out = Message(sender="Test", type=MsgType.NONE, signal=Signal.BEAT, body=None)

        assert out.sender == "Test"
        assert out.type == MsgType.NONE
        assert out.signal == Signal.BEAT
        assert out.body is None

    def test_msgtypetext(self):
        out = Message(sender="Test", type=MsgType.TEXT, signal=Signal.BEAT, body="Test body")

        assert out.sender == "Test"
        assert out.type == MsgType.TEXT
        assert out.signal == Signal.BEAT
        assert out.body == "Test body"

    def test_msgtypestatus(self):
        dtnow = datetime.now()
        statusbody = Status(reqtime=dtnow,
                            status="Test",
                            time=dtnow,
                            statustime=dtnow,
                            statusmessage="Test status")
        out = Message(sender="Test", type=MsgType.STATUS, signal=Signal.BEAT, body=statusbody)

        assert out.sender == "Test"
        assert out.type == MsgType.STATUS
        assert out.signal == Signal.BEAT
        assert out.body == statusbody

    def test_msgtypebytes(self):
        out = Message(sender="Test", type=MsgType.BYTES, signal=Signal.BEAT, body=b'Test message')

        assert out.sender == "Test"
        assert out.type == MsgType.BYTES
        assert out.signal == Signal.BEAT
        assert out.body == b'Test message'

    def test_msgtypemap(self):
        out = Message(sender="Test", type=MsgType.MAP, signal=Signal.BEAT, body={"Test": "Map"})

        assert out.sender == "Test"
        assert out.type == MsgType.MAP
        assert out.signal == Signal.BEAT
        assert out.body == {"Test": "Map"}


class TestStatus:
    def test_fullstatus(self):
        nowdt = datetime.now()
        out = Status(reqtime=nowdt, status="Test", statusmessage="Test", time=nowdt, statustime=nowdt)
        assert out
        assert out.reqtime == nowdt
        assert out.status == "Test"
        assert out.statusmessage == "Test"
        assert out.time == nowdt
        assert out.statustime == nowdt

    def test_nonestatus(self):
        out = Status(reqtime=None, status=None, statusmessage=None, time=None, statustime=None)
        assert out
        assert out.reqtime is None
        assert out.status is None
        assert out.statusmessage is None
        assert out.time is None
        assert out.statustime is None


class TestProducer:
    def test_put(self):
        testq = multiprocessing.Queue()
        producer = ProducerQueue(testq)
        assert testq
        producer.put_nowait("Test1")
        producer.put_nowait("Test2")
        producer.put_nowait("Test3")
        producer.put_nowait("Test4")
        producer.put_nowait("Test5")
        assert testq.get(True, 1.0) == "Test1"
        assert testq.get(True, 1.0) == "Test2"
        assert testq.get(True, 1.0) == "Test3"
        assert testq.get(True, 1.0) == "Test4"
        assert testq.get(True, 1.0) == "Test5"


class TestConsumer:
    def test_get(self):
        testq = multiprocessing.Queue()
        consumer = ConsumerQueue(testq)
        assert consumer
        testq.put_nowait("Test1")
        testq.put_nowait("Test2")
        testq.put_nowait("Test3")
        testq.put_nowait("Test4")
        testq.put_nowait("Test5")
        assert consumer.get(True, 1.0) == "Test1"
        assert consumer.get(True, 1.0) == "Test2"
        assert consumer.get(True, 1.0) == "Test3"
        assert consumer.get(True, 1.0) == "Test4"
        assert consumer.get(True, 1.0) == "Test5"
        with pytest.raises(Empty):
            _ = consumer.get_nowait()


class TestOneWayQueues:
    def test_production(self):
        producer, consumer = generatequeues()
        assert producer
        assert consumer
        assert isinstance(producer, ProducerQueue)
        assert isinstance(consumer, ConsumerQueue)
        producer.put_nowait("Hello")
        assert consumer.get(True, 1.0) == "Hello"

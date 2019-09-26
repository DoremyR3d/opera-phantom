import pickle
from datetime import datetime

from theater.core.constants import Signal, MsgType
from theater.core.messages import Message, Status


class TestMessage:
    def test_msgtypenone(self):
        rick = Message(sender="Test", type=MsgType.NONE, signal=Signal.BEAT, body=None)
        picklerick = pickle.loads(pickle.dumps(rick))

        assert rick == picklerick
        assert picklerick.sender == "Test"
        assert picklerick.type == MsgType.NONE
        assert picklerick.signal == Signal.BEAT
        assert picklerick.body is None

    def test_msgtypetext(self):
        rick = Message(sender="Test", type=MsgType.TEXT, signal=Signal.BEAT, body="Test body")
        picklerick = pickle.loads(pickle.dumps(rick))

        assert picklerick == rick
        assert picklerick.sender == "Test"
        assert picklerick.type == MsgType.TEXT
        assert picklerick.signal == Signal.BEAT
        assert picklerick.body == "Test body"

    def test_msgtypestatus(self):
        dtnow = datetime.now()
        statusbody = Status(reqtime=dtnow,
                            status="Test",
                            time=dtnow,
                            statustime=dtnow,
                            statusmessage="Test status")
        rick = Message(sender="Test", type=MsgType.STATUS, signal=Signal.BEAT, body=statusbody)
        picklerick = pickle.loads(pickle.dumps(rick))

        assert picklerick == rick
        assert picklerick.sender == "Test"
        assert picklerick.type == MsgType.STATUS
        assert picklerick.signal == Signal.BEAT
        assert picklerick.body == statusbody

    def test_msgtypebytes(self):
        rick = Message(sender="Test", type=MsgType.BYTES, signal=Signal.BEAT, body=b'Test message')
        picklerick = pickle.loads(pickle.dumps(rick))

        assert picklerick == rick
        assert picklerick.sender == "Test"
        assert picklerick.type == MsgType.BYTES
        assert picklerick.signal == Signal.BEAT
        assert picklerick.body == b'Test message'

    def test_msgtypemap(self):
        rick = Message(sender="Test", type=MsgType.MAP, signal=Signal.BEAT, body={"Test": "Map"})
        picklerick = pickle.loads(pickle.dumps(rick))

        assert picklerick == rick
        assert picklerick.sender == "Test"
        assert picklerick.type == MsgType.MAP
        assert picklerick.signal == Signal.BEAT
        assert picklerick.body == {"Test": "Map"}

    class TestStatus:
        def test_fullstatus(self):
            nowdt = datetime.now()
            rick = Status(reqtime=nowdt, status="Test", statusmessage="Test", time=nowdt, statustime=nowdt)
            picklerick = pickle.loads(pickle.dumps(rick))

            assert picklerick == rick
            assert picklerick.reqtime == nowdt
            assert picklerick.status == "Test"
            assert picklerick.statusmessage == "Test"
            assert picklerick.time == nowdt
            assert picklerick.statustime == nowdt

        def test_nonestatus(self):
            rick = Status(reqtime=None, status=None, statusmessage=None, time=None, statustime=None)
            picklerick = pickle.loads(pickle.dumps(rick))

            assert picklerick == rick
            assert picklerick.reqtime is None
            assert picklerick.status is None
            assert picklerick.statusmessage is None
            assert picklerick.time is None
            assert picklerick.statustime is None
    pass

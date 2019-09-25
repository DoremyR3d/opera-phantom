# -*- coding: utf-8 -*-

import pytest

from theater.core.errors import IllegalActionException
from theater.core.messages import MessageFactory


class TestBasics:
    def test_import(self):
        assert True

    def test_instance(self):
        from theater.core.messages import Message
        with pytest.raises(IllegalActionException):
            _ = Message()
        msgfact = MessageFactory("TestSender")
        assert msgfact
        assert isinstance(msgfact, MessageFactory)

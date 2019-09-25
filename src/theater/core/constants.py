import enum

__all__ = ['SENDER_KEY', 'SIGNAL_KEY', 'MSGTYPE_KEY',
           'HB_REQTIME', 'HB_STATUS', 'HB_TIME', 'HB_STATUSTIME', 'HB_STATUSMESSAGE',
           'Signal', 'MsgType']

# --------------------
# Simple constants
# --------------------

SENDER_KEY: str = 'Sender'
SIGNAL_KEY: str = 'Signal'
MSGTYPE_KEY: str = 'MsgType'

HB_REQTIME = 'hb_reqtime'
HB_STATUS = 'hb_status'
HB_TIME = 'hb_time'
HB_STATUSTIME = 'hb_statustime'
HB_STATUSMESSAGE = 'hb_statusmessage'


# --------------------
# Enumerative constants
# --------------------


class Signal(enum.Enum):
    """Enum that contains all possibile signals stored in a Message's header"""
    CREATE = 'CREATE'
    INTERRUPT = 'INTERRUPT'
    BEAT = 'BEAT'
    KILL = 'KILL'
    UPDATE = 'UPDATE'
    TRIGGER = 'TRIGGER'


class MsgType(enum.Enum):
    """Enum that contains all possibile type for a Message's body"""
    NONE = "None"
    TEXT = "Text"
    MAP = "Map"
    STATUS = "Status"
    BYTES = "Bytes"

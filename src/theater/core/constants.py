import enum

__all__ = ['Signal', 'MsgType']

# --------------------
# Simple constants
# --------------------

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

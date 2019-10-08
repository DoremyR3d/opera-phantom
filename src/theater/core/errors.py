import attr


@attr.s(auto_exc=True)
class IllegalValueException(Exception):
    msg = attr.ib()


@attr.s(auto_exc=True)
class IllegalActionException(Exception):
    msg = attr.ib()


@attr.s(auto_exc=True)
class ScoreEnd(Exception):
    msg = attr.ib()

import attr


@attr.s(auto_exc=True)
class IllegalValueException(Exception):
    pass


@attr.s(auto_exc=True)
class IllegalActionException(Exception):
    pass


@attr.s(auto_exc=True)
class ScoreEnd(Exception):
    pass

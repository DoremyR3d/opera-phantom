import logging

__all__ = ['LOGNAME', 'LOGLEVEL', 'LOGCONSOLE', 'LOGFILE', 'LOGFORMAT', 'LOGDATEFMT',
           'Loggable']

# --------------------
# Module Attributes
# --------------------

LOGNAME: str = 'logname'
LOGLEVEL: str = 'loglevel'
LOGCONSOLE: str = 'logconsole'
LOGFILE: str = 'logfile'
LOGFORMAT: str = 'logformat'
LOGDATEFMT: str = 'logdatefmt'


# --------------------
# Module Classes
# --------------------


class Loggable:
    """Logging trait"""
    __slots__ = ('__logger__',)

    def __init__(self):
        self.__logger__ = None

    def init_logger(self, logconf: dict):
        name = logconf.get(LOGNAME)
        level = logconf.get(LOGLEVEL)
        console = logconf.get(LOGCONSOLE)
        file = logconf.get(LOGFILE)
        logfmt = logconf.get(LOGFORMAT)
        timefmt = logconf.get(LOGDATEFMT)

        # Step 1: handlers
        handlers = []
        if console == 'True':
            handlers.append(logging.StreamHandler())
        if file:
            handlers.append(logging.FileHandler(file, 'a+', 'utf-8'))
        if level:
            for handler in handlers:
                handler.setLevel(logging.getLevelName(level))
        if logfmt:
            for handler in handlers:
                handler.setFormatter(logging.Formatter(fmt=logfmt, datefmt=timefmt))
        self.__logger__ = logging.getLogger(name)
        for handler in handlers:
            self.__logger__.addHandler(handler)

    def info(self, msg, *args):
        if self.__logger__:
            self.__logger__.info(msg, args)

    def debug(self, msg, *args):
        if self.__logger__:
            self.__logger__.debug(msg, args)

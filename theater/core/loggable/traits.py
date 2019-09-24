import logging
from abc import ABC, abstractmethod

from theater.core.loggable.constants import LOGNAME, LOGLEVEL, LOGCONSOLE, LOGFILE, LOGFORMAT, LOGDATEFMT


class Loggable(ABC):
    """Logging trait"""
    __slots__ = ()

    def __init__(self):
        self._logger = None

    @property
    @abstractmethod
    def _logger(self) -> logging.Logger:
        pass

    @_logger.setter
    @abstractmethod
    def _logger(self, new_logger: logging.Logger):
        pass

    def _initlogger(self, logconf: dict):
        name = logconf.get(LOGNAME)
        level = logconf.get(LOGLEVEL)
        console = logconf.get(LOGCONSOLE)
        file = logconf.get(LOGFILE)
        logfmt = logconf.get(LOGFORMAT)
        timefmt = logconf.get(LOGDATEFMT)

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
        self._logger = logging.getLogger(name)
        for handler in handlers:
            self._logger.addHandler(handler)

    def _error(self, msg, *args):
        if self._logger:
            self._logger.error(msg, args)

    def _warn(self, msg, *args):
        if self._logger:
            self._logger.warning(msg, args)

    def _info(self, msg, *args):
        if self._logger:
            self._logger.info(msg, args)

    def _debug(self, msg, *args):
        if self._logger:
            self._logger.debug(msg, args)

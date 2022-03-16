"""
Title       : Logger
Description : Defines class logger, which implements a custom logger.
Author      : Bernardo Paulsen
Version     : 1.0.0
"""
import logging


class Logger:
    """
    Class which implements a custom logger.

    :param name: Logger name
    :type name: str
    :param file: Log file name, defaults to "log"
    :type file: str, optional
    :param level: Log level, defaults to logging.DEBUG
    :type level: int, optional
    :param mode: Log file mode, defaults to "a"
    :type mode: str, optional
    :param format_: Log format, defaults to "%(asctime)s:%(name)s:%(levelname)s:%(message)s"
    :type format_: str, optional
    """

    def __init__(self,
                 name: str,
                 file: str = "log",
                 level: int = logging.DEBUG,
                 mode: str = "a",
                 format_: str = "%(asctime)s::%(name)s::%(levelname)s::%(message)s"):
        """
        Constructor method.
        """
        self.logger = self.config(name, file, level, mode, format_)
        self.debug = self.logger.debug
        self.warning = self.logger.warning
        self.error = self.logger.error

    @staticmethod
    def console_handler(level: int,
                        formatter: logging.Formatter):
        """
        Configures console handler.

        :param level: Log level
        :type level: int
        :param formatter: Formatter
        :type formatter: logging.Formatter

        :return: Console handler
        :rtype: logging.StreamHandler
        """
        handler = logging.StreamHandler()
        handler.setLevel(level)
        handler.setFormatter(formatter)
        return handler

    @staticmethod
    def file_handler(file: str,
                     mode: str,
                     level: int,
                     formatter: logging.Formatter):
        """
        Configures file handler.

        :param file: Log file name
        :type file: str
        :param mode: Log mode
        :type mode: str
        :param level: Log level
        :type level: int
        :param formatter: Formatter
        :type formatter: logging.Formatter

        :return: File handler
        :rtype: logging.FileHandler
        """
        handler = logging.FileHandler(
            filename=file,
            mode=mode)
        handler.setLevel(level)
        handler.setFormatter(formatter)
        return handler

    @staticmethod
    def formatter(format_: str):
        """
        Configures formatter.

        :param format_: Log format
        :type format_: str
        """
        formatter = logging.Formatter(format_)
        return formatter

    def config(self,
               name: str,
               file: str,
               level: int,
               mode: str,
               format_: str):
        """
        Configures logger.

        :param name: Logger name
        :type name: str
        :param file: Log file name
        :type file: str
        :param level: Log level
        :type level: int
        :param mode: Log file mode
        :type mode: str
        :param format_: Log format
        :type format_: str
        
        :return: Logger
        :rtype: logging.Logger
        """

        formatter = self.formatter(format_)
        logger = logging.getLogger(name)
        console_handler = self.console_handler(level, formatter)
        file_handler = self.file_handler(f"logs/{file}.log", mode, level, formatter)
        logger.setLevel(level)
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        logger.debug("logger configured")
        return logger


if __name__ == "__main__":
    log = Logger("logger")

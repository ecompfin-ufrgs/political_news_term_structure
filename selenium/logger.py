import logging

class Logger:
    def __init__(
        self,
        name   : str,
        file   : str = "log.log",
        level  : int = logging.DEBUG,
        mode   : str = "a",
        format : str = "%(asctime)s:%(name)s:%(levelname)s:%(message)s"):

        self.logger = self.config(name, file, level, mode, format)
        self.debug  = self.logger.debug

    def console_handler(self,
        level     : int,
        formatter : logging.Formatter):

        handler = logging.StreamHandler()
        handler.setLevel(level)
        handler.setFormatter(formatter)
        return handler

    def file_handler(self,
        file      : str,
        mode      : str,
        level     : int,
        formatter : logging.Formatter):

        handler = logging.FileHandler(
            filename = file,
            mode     = mode)
        handler.setLevel(level)
        handler.setFormatter(formatter)
        return handler

    def formatter(self,
        format : str):

        formatter = logging.Formatter(format)
        return formatter

    def config(self,
        name   : str,
        file   : str = "log.log",
        level  : int = 0,
        mode   : str = "w",
        format : str = "%(asctime)s:%(name)s:%(levelname)s:%(message)s"):

        formatter       = self.formatter(format)
        logger          = logging.getLogger(name)
        console_handler = self.console_handler(level,formatter)
        file_handler    = self.file_handler(file,mode,level,formatter)
        logger.setLevel(level)
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        logger.debug("logger configured")
        return logger

if __name__ == "__main__":
    log = Logger("logger test")
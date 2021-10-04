import logging


class Logger:
    """
    Implements custom logger.
    """
    MODE: str = "a"
    LEVEL: int = logging.DEBUG
    FORMAT: str = "%(asctime)s::%(name)s::%(levelname)s::%(message)s"
    
    def __init__(self,
                 name: str,
                 file_name: str
                 ) -> None:
        """
        Initiator method.

        :param name: Logger name
        :type name: str
        :param file_name: Log file name
        :type file_name: str
        """
        self.name: str = name
        self.file_name: str = file_name
        
        self.logger: logging.Logger = self.get_logger()
        
        self.debug: logging.Logger.debug = self.logger.debug
        self.info: logging.Logger.info = self.logger.info
        self.warning: logging.Logger.warning = self.logger.warning
        self.error: logging.Logger.error = self.logger.error
        self.critical: logging.Logger.critical = self.logger.critical
        
    def get_logger(self) -> logging.Logger:
        """
        Returns custom logger with stream and file handlers.
            
        :return: Custom logger
        :rtype: logging.Logger
        """
        formatter = logging.Formatter(self.FORMAT)
        logger = logging.getLogger(self.name)
        logger.setLevel(self.LEVEL)
        stream_handler = logging.StreamHandler()
        file_handler = logging.FileHandler(self.file_name, self.MODE)
        for handler in [stream_handler, file_handler]:
            handler.setLevel(self.LEVEL)
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger

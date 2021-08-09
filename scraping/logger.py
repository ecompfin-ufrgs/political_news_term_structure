"""
Title: Logger Class
Description: Class which manages a custom logger.
Version: 0.0.1
Author: Bernardo Paulsen
"""


import logging


class Logger:
    
    MODE = "a"
    LEVEL = logging.DEBUG
    FORMAT = "%(asctime)s::%(name)s::%(levelname)s::%(message)s"
    
    def __init__(self,
        name,
        filename):
            
        self.name = name
        self.filename = filename
        
        self.logger = self.get_logger()
        
        self.debug = self.logger.debug
        self.warning = self.logger.warning
        self.error = self.logger.error
        
    def get_logger(self):
        
        formatter = logging.Formatter(self.FORMAT)
        logger = logging.getLogger(self.name)
        logger.setLevel(self.LEVEL)
        
        stream_handler = logging.StreamHandler()
        file_handler = logging.FileHandler(self.filename, self.MODE)
        
        for handler in [stream_handler, file_handler]:
            handler.setLevel(self.LEVEL)
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
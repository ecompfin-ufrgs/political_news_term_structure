"""
Title: Logger Class
Description: Class which manages a custom logger.
Version: 0.0.1
Author: Bernardo Paulsen
"""


import logging


class Logger:
    
    def __init__(self,
        name,
        filename):
            
        self.name = name
        self.filename = filename
        self.mode = "a"
        self.level = logging.DEBUG
        self.format = "%(asctime)s::%(name)s::%(levelname)s::%(message)s"
        
        self.logger = self.get_logger()
        
        self.debug = self.logger.debug
        self.warning = self.logger.warning
        self.error = self.logger.error
        
    def get_logger(self):
        
        formatter = logging.Formatter(self.format)
        logger = logging.getLogger(self.name)
        logger.setLevel(self.level)
        
        for h_class in [logging.StreamHandler, logging.FileHandler]:
            handler = h_class(self.filename, self.mode)
            handler.setLevel(self.level)
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
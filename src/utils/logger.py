import logging
import sys


class CustomLogger(logging.LoggerAdapter):
    """"Customized logger with auxiliary methods to display log messages."""

    def __init__(self, module_name):
        self.module_name = module_name
        self.logger = logging.getLogger(self.module_name)
        super(CustomLogger, self).__init__(self.logger, {})

    def get_logger(self):
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        return self.logger

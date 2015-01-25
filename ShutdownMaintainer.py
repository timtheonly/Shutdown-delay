__author__ = 'Daniel Hogan'

import subprocess
from datetime import datetime 


class ShutdownMaintainer:
    """
    Maintains a pre-existing shutdown

    Attributes:
        logger -- the log handler to be used"""
    def __init__(self, logger):
        self.logger = logger

    def cancel_shutdown(self):
        """"
            Cancels an existing shutdown

            Throws:
                Shutdown when shutdown cannot be canceled (i.e. no shutdown exists)"""
        self.exitcode = subprocess.call(['shutdown', '-c'])
        if self.exitcode == 0:
            self.logger.log('shutdown canceled')
            return
        self.logger.log('failed to cancel shutdown')
        raise ShutdownException('failed to cancel shutdown')

    def set_shutdown(self, delay):
        """"
            Sets a Shutdown for NOW + delay
            Args:
                delay -- The delay to be used for the shutdown

            Throws:
                Shutdown when shutdown cannot be set (i.e. a shutdown already exits)
        """
        d = datetime.now()
        hr = d.hour
        hr = hr+1
        hr = hr+delay
        hr = hr%24
        hour_arg = '{0}:00'.format(hr)
        exitcode = subprocess.call(['shutdown', '-h', hour_arg])
        if exitcode == 0:
            self.logger.log('shutdown delayed until {0}:00'.format(hr))
            return
        self.logger.log('failed to set shutdown')
        raise ShutdownException('failed to set shutdown')


class ShutdownException(Exception):
    """Exception raised for errors in ShutdownMaintainer

    Attrinbutes:
        exceptString -- explanation of the error"""
    def __init__(self, except_string):
        self.except_string = except_string

    def __str__(self):
        return repr(self.exceptString)
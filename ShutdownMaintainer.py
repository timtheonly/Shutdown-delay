import subprocess
from datetime import datetime 


class ShutdownMaintainer:
    def __init__(self, logger):
        self.logger = logger

    def cancel_shutdown(self):
            exitcode = subprocess.call(['shutdown', '-c'])
            if exitcode == 0:
                self.logger.log('shutdown canceled')
                return
            self.logger.log('failed to cancel shutdown')
            raise ShutDownException('failed to cancel shutdown')

    def set_shutdown(self, delay):
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
            raise ShutDownException('failed to set shutdown')


class ShutDownException(Exception):
    """Exception raised for errors in ShutdownMaintainer

    Attrinbutes:
        exceptString -- explanation of the error"""
    def __init__(self, except_string):
        self.except_string = except_string

    def __str__(self):
        return repr(self.exceptString)
import subprocess
from datetime import datetime 


class shutdown_maintainer:
    def __init__(self, logger):
        self.logger = logger

    def cancel_shutdown(self):
            exitcode = subprocess.call(['shutdown', '-c'])
            if exitcode == 0:
                self.logger.log('shutdown canceled')
                return 0
            self.logger.log('failed to cancel shutdown')
            return 1

    def set_shutdown(self, delay):
            d = datetime.now()
            hr = d.hour
            hr = hr + 1
            hr = hr+delay
            hr = hr % 24
            hour_arg = '{0}:00'.format(hr)
            exitcode = subprocess.call(['shutdown', '-h', hour_arg])
            if exitcode == 0:
                self.logger.log('shutdown delayed until {0}:00'.format(hr))
                return 0
            self.logger.log('failed to set shutdown')
            return 0

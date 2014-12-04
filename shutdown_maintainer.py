import subprocess
from datetime import datetime 

class shutdown_maintainer:
    
    def cancel_shutdown(self):
            exitcode = subprocess.call(['shutdown' ,'-c']) 
            d = datetime.now()                    
            if exitcode == 0:
                self.log('shutdown canceled')
                return 0
            self.log('failed to cancel shutdown')
            return 1

    def set_shutdown(self, delay):
            d = datetime.now()
            hr = d.hour
            hr = hr +1
            hr = hr+delay
            hr = hr % 24
            hourarg = '{0}:00'.format(hr)
            exitcode = subprocess.call(['shutdown' ,'-h',hourarg])
            if exitcode == 0:
                self.log('shutdown delayed until {0}:00'.format(hr))
                return 0
            self.log('failed to set shutdown')
            return 0

    def log(self, message):
            d = datetime.now()
            log = open('shutdown.log', 'a')
            log.write('{0} - {1}\n'.format(datetime.strftime(d,'%a-%H:%M:%S-%d/%m/%y'), message))
            return


__author__ = 'daniel'

from datetime import datetime


class Logger:
    def __init__(self, filename):
        self.logFile = open(filename, 'a')

    def log(self, message):
        d = datetime.now()
        self.logFile.write('{0} -- {1}\n'.format(datetime.strftime(d,'%a-%H:%M:%S-%d/%m/%y'), message))

    def close(self):
        if not self.logFile.closed:
            self.logFile.close()

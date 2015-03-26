__author__ = 'Daniel Hogan'

from datetime import datetime


class Logger:
    """
        Maintains a log file

        Attributes
            logFile -- the file to use
            d -- the current datetime
    """
    def __init__(self, filename):
        self.logFile = open(filename, 'a')
        self.d = datetime.now()

    def log(self, message):
        """
            logs the given message to the logfile
        Args:
         message -- message to be written to the log file

        """
        self.d = datetime.now()
        self.logFile.write('{0} -- {1}\n'.format(self.d.strftime('%a-%d/%m/%y-%H:%M:%S'), message))

    def close(self):
        """
            Closes the log file if its open

        """
        if not self.logFile.closed:
            self.logFile.write('\n')
            self.logFile.close()

__author__ = 'Daniel Hogan'

from datetime import datetime


class Logger:
    """
        Maintains a log file

        Attributes
            app_name -- the name of the app we're logging for
            d -- the current datetime
    """
    def __init__(self, app_name,log_dir):
        self.d = datetime.now()
        file_name = "{0}{1}_{2}.log".format(log_dir,app_name,self.d.strftime('%d%m%y'))
        self.logFile = open(file_name, 'a')

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

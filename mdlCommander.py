###############################################################################
# Script by rawad.kharma@wdc.com
# Reliability team tefen,il
###############################################################################
# rel commander 
# library for scripts and jobs 
# Ver Beta 0.0.1

import os,sys
import logging
import csv,json

try:
    import pypyodbc
except ImportError as e:
    try:
        from pip._internal import main as pipmain
    except ImportError as e:
        from pip import main as pipmain
    finally:
        pipmain(['install', 'pypyodbc'])

class clsCommander(object):
    _instance = None
    def __new__(self):
        if not self._instance:
            print('Creating new instance')
            self._instance = super(clsCommander,self).__new__(self)
        return self._instance

    def fnLogger(self, logLevel = "INFO", log_file = "run_log.txt", name=None):
        '''
        #init the logger
        default log file "run_log.txt"
        default log level in INFO 
            can use [DEBUG, INFO, WARNING, ERROR, CRITICAL]
        return: OBJ logging
        '''
        logging.getLogger().setLevel(logging.NOTSET)
        # set debug level for log file
        reLogFileHandler = logging.FileHandler(log_file)
        reLogFileHandler.setLevel(logging.DEBUG) # default debug level in log files DEBUG
        reLogFileHandler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] [%(module)s] %(name)s : %(message)s"))
        logging.getLogger().addHandler(reLogFileHandler)          # log to file

        # set debug level for STDOUT terminal output
        reLogStreamHandler = logging.StreamHandler(sys.stdout)
        reLogStreamHandler.setLevel(logLevel.upper())
        reLogStreamHandler.setFormatter(logging.Formatter("[%(levelname)s] [%(module)s] - %(name)s : %(message)s"))
        logging.getLogger().addHandler(reLogStreamHandler)        # log to STDOUT

        self.logger = logging.getLogger( name if name else __name__)
        return self.logger

    def fnDBConnect(self, uid, pwd, server, db):
        '''
        # config and INIT DB connection
        return: OBJ database connection cursor
        '''
        try:
            if sys.platform == "win32":
                strConnection = "Driver={SQL Server};Server=%s;uid=%s;pwd=%s; database=%s" % (str(server),uid,pwd,db)
                self.logger.info("connection string: %s" % strConnection)
                connection = pypyodbc.connect(strConnection)
            else:
                strConnection = "Driver={ODBC Driver 17 for SQL Server};Server=%s;uid=%s;pwd=%s; database=%s" % (str(server),uid,pwd,db)
                self.logger.info("connection string: %s" % strConnection)
                connection = pypyodbc.connect(strConnection)
                connection.unicode_results = True
        except Exception as SQLServerException:
            self.logger.exception("DB connection failed \n\t %s" % SQLServerException)
            sys.exit(1)

        return connection.cursor()

    def fnCSVWrite(self, lines, CSV_HEADER=None, filename=None):

        if filename is None:
            self.logger.error("You need to pass a file name")
            return None

        with open(filename, 'wb') as csvFile:
            writer = csv.writer(csvFile)
            if CSV_HEADER:
                writer.writerow([column[0] for column in CSV_HEADER])
            for line in lines:
                writer.writerow(line)
        self.logger.info("[CSV] file written [%s] with [%d] Rows" % (filename, len(lines)))
###############################################################################################
objCMD = clsCommander()
fnLogger = clsCommander().fnLogger
fnDBConnect = clsCommander().fnDBConnect
fnCSVWrite = clsCommander().fnCSVWrite
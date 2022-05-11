from mdlCommander import objCMD

# Init the logger 
logger = objCMD.fnLogger(name='tests',logLevel="info") #name='tests',log_file="test1.log",logLevel="info"

logger.info("this is info logging")
logger.error("This is error messege")
logger.debug("this debug msg default is write to file no STDOUT")

# Init database connection
dbCurser = objCMD.fnDBConnect("user","pass","host","dbname")
dbCurser.execute("SELECT 1 as 1")
results = dbCurser.fetchall()

logger.info("Fetched from db A %s" % str(len(results)))


# Init CSV file writer
objCMD.fnCSVWrite(results,dbCurser.description, "test.csv")
logger.debug("[DEBUG Query results] %s" % results)
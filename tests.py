from mdlCommander import objCMD


# Init the logger 
logger = objCMD.fnLogger(name='tests',logLevel="info") #name='tests',log_file="test1.log",logLevel="info"

SideAdbCurser = objCMD.fnDBConnect("Ace","Ace2018!","10.24.8.188","REL_Side_A_39")
SideBdbCurser = objCMD.fnDBConnect("Ace","Ace2018!","10.24.8.188","REL_Side_B_49")

SQL = """
SELECT TOP (1000) [ID]
      ,[Section]
      ,[Parameter]
      ,[Value]
      ,[LabId]
      ,[DataType]
      ,[Description]
      ,[isVisible]
      ,[RV]
      FROM [dbo].[ACEClientConfiguration]
"""
logger.debug("[SQL Query] %s",SQL)

SideAdbCurser.execute(SQL)
SideBdbCurser.execute(SQL)

resultsA = SideAdbCurser.fetchall()
resultsB = SideBdbCurser.fetchall()

logger.info("Fetched from db A %s" % str(len(resultsA)))
objCMD.fnCSVWrite(resultsA,SideAdbCurser.description, "testA.csv")
# logger.debug("[DEBUG Query results] %s" % resultsA)

logger.info("Fetched from db B %s" % str(len(resultsB)))
objCMD.fnCSVWrite(resultsB,SideBdbCurser.description, "testB.csv")
# logger.debug("[DEBUG Query results] %s" % resultsB)





from Validation import Validation
from ReadData import ReadData

import os
import csv
from dotenv import load_dotenv



# Defines local directory to allow for relative pathing across any device running the code
CurrentDirectory = os.path.dirname(__file__)
RootDirectory = os.path.join(CurrentDirectory, "..")

# load from SQL.env
env_path = os.path.join('SQL-Integration', 'SQL.env')
load_dotenv(dotenv_path=env_path)
StorageType = os.getenv("StorageType")


## ################## ##
## Global Access Code ##
## ################## ##

if StorageType == "SQL":
    ValidDatabase = ReadData.CheckSQLConnection()
    if True:
        ReadData.ReadSQLTable()
    
elif StorageType == "CSV":
    CSVFilePath = os.path.join(RootDirectory, "FirewallRules.csv")
    OpenCSV(CSVFilePath)



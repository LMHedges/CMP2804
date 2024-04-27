from Validation import Validation
from ReadData import ReadData
from ModifyTable import ModifyTable
from User_CLI import run_user_cli

import os
import csv
import mysql.connector
from dotenv import load_dotenv

Query = ['101', '192.168.1.1', 'Allow', 'TCP', 10]

# Defines local directory to allow for relative pathing across any device running the code
CurrentDirectory = os.path.dirname(__file__)
RootDirectory = os.path.join(CurrentDirectory, "..")

# load from SQL.env
env_path = os.path.join('SQL-Integration', 'SQL.env')
load_dotenv(dotenv_path=env_path)
StorageType = os.getenv("StorageType")
InputUserFormat = os.getenv("InputUserFormat")

# Verify connectivity and data integrity
if StorageType == "SQL":
    ValidDatabase = ReadData.CheckSQLConnection()
    

# initiating classes
ModifyTable_instance = ModifyTable(StorageType)
InsertRow_instance = ModifyTable_instance.InsertRow(ModifyTable_instance)
InsertRow_instance.insert(Query)


if StorageType == "SQL":
    ValidDatabase = ReadData.CheckSQLConnection()
    if True:
        ReadData.ReadSQLTable()
    
elif StorageType == "CSV":
    CSVFilePath = os.path.join(RootDirectory, "FirewallRules.csv")
    ReadData.OpenCSV(CSVFilePath)
   
# Runs User based CLI format function assuming environmental variable is set to user    
if InputUserFormat == "User":
    run_user_cli(InputUserFormat, StorageType)
    




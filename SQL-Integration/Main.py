from ModifyTable import ModifyTable
from interface_handling.User_CLI import UserCLI
from connection_handling.DatabaseConnection import DatabaseConnection

import os
import csv
import pymysql
from dotenv import load_dotenv

# Defines local directory to allow for relative pathing across any device running the code
CurrentDirectory = os.path.dirname(__file__)
RootDirectory = os.path.join(CurrentDirectory, "..")

# load from SQL.env
env_path = os.path.join('SQL-Integration', 'SQL.env')
load_dotenv(dotenv_path=env_path)
StorageType = os.getenv("StorageType")
InputUserFormat = os.getenv("InputUserFormat")

# Setup database connection and cursor
db_connection = DatabaseConnection()
connection = db_connection.connect_and_initialize() 
cursor = connection.cursor()

# initiating classes
ModifyTable_instance = ModifyTable(StorageType, cursor)
InsertRow_instance = ModifyTable_instance.InsertRow(ModifyTable_instance)


if StorageType == "SQL":
    print("SQL chosen")
    
    
elif StorageType == "CSV":
    print("CSV chosen")
    CSVFilePath = os.path.join(RootDirectory, "FirewallRules.csv")
   
# Runs User based CLI format function assuming environmental variable is set to user    
if InputUserFormat == "User":
    UserCLI(connection) # default __init__ function passing connection object to UserCLI class
    UserCLI(connection).collect_data() # prompts user for data input
    




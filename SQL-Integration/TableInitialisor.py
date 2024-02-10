import os
import sqlite3
import csv
from dotenv import load_dotenv
import mysql.connector 



# Defines local directory to allow for relative pathing across any device running the code
CurrentDirectory = os.path.dirname(__file__)
RootDirectory = os.path.join(CurrentDirectory, "..")

# load from SQL.env
env_path = os.path.join('SQL-Integration', 'SQL.env')
load_dotenv(dotenv_path=env_path)
StorageType = os.getenv("StorageType")




# Attempt to import table or create one if it doesn't exist
def CreateDatabaseIfNotExists():
    RulesetDatabase = sqlite3.connect("RulesetDatabase.db")
    Cursor = RulesetDatabase.cursor()
    
    # Create table if it doesn't exist
    Cursor.execute(''' 
                   
    CREATE TABLE IF NOT EXISTS FirewallRules
    (
        RuleID INT PRIMARY KEY,
        IP_Address TEXT,
        Action TEXT NOT NULL,
        Protocol TEXT NOT NULL, 
        Weighting INTEGER DEFAULT -1,
        CHECK(action IN ('Allow', 'Deny', 'Bypass'))
        CHECK(protocol IN ('TCP', 'UDP', 'ALL'))
    );
    ''')
    


## ############################ ## 
## reading from table data ONLY ## 
## ############################ ## 

# Loads csv table into primary memory allowing quick read access
def OpenCSV(CSVFilePath):
    print("CSV Format File Storage has been selected")
    with open('FirewallRules.csv', 'r') as CSVFilePath:
        TableData = csv.reader(CSVFilePath)
        for record in TableData:
            print(record)
         

# Validates if SQL credentials are valid
def CheckSQLConnection():
    print("SQL Storage has been selected")
    try:
        mydb = mysql.connector.connect(
            host = os.getenv("SQLHost"),
            port = os.getenv("SQLPort"),
            user = os.getenv("SQLUser"),
            passwd = os.getenv("SQLPassword"),
            database = os.getenv("rulesetdatabase")
        )
        print("Valid SQL connection credentials provided")
       
        CreateDatabaseIfNotExists() # Creates a table for the firewall rules if it doesn't already exist
        return True
    except:
        print("Valid SQL connection credentials NOT provided")
        return False
        
# Reads from SQL table and prints all records
def ReadSQLTable():
    print("Reading from SQL Table...")
    try:
        # Establish a new connection using environment variables
        mydb = mysql.connector.connect(
            host=os.getenv("SQLHost"),
            port=os.getenv("SQLPort"),
            user=os.getenv("SQLUser"),
            passwd=os.getenv("SQLPassword"),
            database=os.getenv("rulesetdatabase")  # Ensure this is the correct env variable for the database name
        )
        cursor = mydb.cursor()

        # Execute SQL query to fetch all records from FirewallRules
        cursor.execute("USE rulesetdatabase")
        cursor.execute("SELECT * FROM FirewallRules")

        # Fetch all rows from the last executed query
        records = cursor.fetchall()

        # Check if there are records to print, otherwise state it's empty
        if records:
            print("Displaying all records from FirewallRules:")
            for record in records:
                print(record)
        else:
            print("No records found in FirewallRules.")

        # Close the cursor and connection
        cursor.close()
        mydb.close()

    except mysql.connector.Error as err:
        print(f"Error reading from MySQL table: {err}")
    
    
    


## ####################################################### ##
## Purely for validation of new entries and existing data  ##
## ####################################################### ## 

# Check if an IP is a valid ipv4 address
def IPChecker(IP_Address):
    try:
        ipaddress.ip_address(IP_Address)
        return True
    except ValueError:
        Print ("Invalid IP Address")
        return False
    


## ######################################################### ## 
## Modifying actions eg deleting, updating, adding new rules ##
## ######################################################### ##





## ################## ##
## Global Access Code ##
## ################## ##

if StorageType == "SQL":
    ValidDatabase = CheckSQLConnection()
    if True:
        ReadSQLTable()
    
elif StorageType == "CSV":
    CSVFilePath = os.path.join(RootDirectory, "FirewallRules.csv")
    OpenCSV(CSVFilePath)



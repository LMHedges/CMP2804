import os
import sqlite3
import csv
import dotenv


# Attempt to import table or create one if it doesn't exist
#RulesetDatabase = sqlite3.connect("RulesetDatabase.db")
#Cursor = RulesetDatabase.cursor()

# load from SQL.env
load_dotenv()
StorageType = os.getenv("StorageType", "CSV")


# Attempt to import table or create one if it doesn't exist
def AccessTable():
    RulesetDatabase = sqlite3.connect("RulesetDatabase.db")
    Cursor = RulesetDatabase.cursor()
    
    # Create table if it doesn't exist
    cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS FirewallRules
    (
        IP_Adress TEXT PRIMARY KEY,
        action TEXT NOT NULL,
        protocol TEXT NOT NULL, 
        Weighting INTEGER DEFAULT -1,
        CHECK(action IN ('Allow', 'Deny', 'Bypass'))
        CHECK(protocol IN ('TCP', 'UDP', 'ALL'))
        CHECK (ip_address ~ '^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$')
    );
    ''')
    
    





# Check if an IP is a valid ipv4 address
def IPChecker(IP_Address):
    try:
        ipaddress.ip_address(IP_Address)
        return True
    except ValueError:
        Print ("Invalid IP Address")
        return False
    






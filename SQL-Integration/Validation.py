## ####################################################### ##
## Purely for validation of new entries and existing data  ##
## ####################################################### ## 

class Validation:

    # Check if an IP is a valid ipv4 address
    def IPChecker(IP_Address):
        try:
            ipaddress.ip_address(IP_Address)
            return True
        except ValueError:
            Print ("Invalid IP Address")
            return False
        
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

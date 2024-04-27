import ipaddress
import sqlite3


####################################
## ONLY to be used for validation ##
####################################
class Validation:
    
    @staticmethod
    def check_ip_address(ip_address):
        """Check if an IP is a valid IPv4 address."""
        try:
            ipaddress.ip_address(ip_address)
            return True
        except ValueError:
            print("Invalid IP Address")
            return False

    @staticmethod
    def check_action(action):
        """Validate action to be one of the specified options."""
        valid_actions = {'Allow', 'Deny', 'Bypass'}
        if action in valid_actions:
            return True
        print("Invalid Action")
        return False

    @staticmethod
    def check_protocol(protocol):
        """Validate protocol to be one of the specified options."""
        valid_protocols = {'TCP', 'UDP', 'ALL'}
        if protocol in valid_protocols:
            return True
        print("Invalid Protocol")
        return False

    @staticmethod
    def check_weighting(weighting):
        """Validate weighting to be a non-negative integer."""
        try:
            weight = int(weighting)
            if weight >= 0:
                return True
            print("Weighting must be a non-negative integer.")
        except ValueError:
            print("Weighting must be an integer.")
        return False

    @staticmethod
    def create_database_if_not_exists():
        """Attempt to create a database table for firewall rules if it doesn't already exist."""
        ruleset_database = sqlite3.connect("RulesetDatabase.db")
        cursor = ruleset_database.cursor()
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS FirewallRules
            (
                RuleID INTEGER PRIMARY KEY AUTOINCREMENT,
                IP_Address TEXT,
                Action TEXT NOT NULL,
                Protocol TEXT NOT NULL, 
                Weighting INTEGER DEFAULT -1,
                CHECK(Action IN ('Allow', 'Deny', 'Bypass')),
                CHECK(Protocol IN ('TCP', 'UDP', 'ALL'))
            );
        ''')
        ruleset_database.commit()
        ruleset_database.close()

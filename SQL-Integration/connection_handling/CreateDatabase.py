from connection_handling.DatabaseConnection import DatabaseConnection

class CreateTable:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = self.connection.cursor()

    def create_firewall_rules_table(self):
        """Create the FirewallRules table if it does not exist."""
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS FirewallRules (
                RuleID INT AUTO_INCREMENT PRIMARY KEY,
                IP_Address VARCHAR(15) NOT NULL,
                Action ENUM('Allow', 'Deny', 'Bypass') NOT NULL,
                Protocol ENUM('TCP', 'UDP', 'ALL') NOT NULL,
                Weighting INT DEFAULT -1,
                CHECK (Weighting >= -1)
            );
        '''
        self.cursor.execute(create_table_query)
        self.connection.commit()
        print("FirewallRules table created or already exists.")

    def close_cursor(self):
        """Close the database cursor."""
        self.cursor.close()

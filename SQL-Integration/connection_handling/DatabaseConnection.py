import pymysql
from dotenv import load_dotenv
import os

class DatabaseConnection:
    
    # Pulls credentials from sql.env - will use default values otherwise
    def __init__(self):
        self.host = os.getenv('SQLHost')
        self.port = int(os.getenv('SQLPort'))
        self.user = os.getenv('SQLUser')
        self.password = os.getenv('SQLPassword')
        self.database = os.getenv('SQLDatabase')

    def connect(self):
        try:
            # Attempt to connect to the specified database
            return pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database, port=self.port, charset='utf8mb4')
        except pymysql.err.OperationalError as e:
            if e.args[0] == 1049:
                # If the database does not exist, connect without specifying a database
                connection = pymysql.connect(host=self.host, user=self.user, password=self.password, port=self.port, charset='utf8mb4')
                with connection.cursor() as cursor:
                    # Create the database
                    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
                connection.commit()
                connection.close()

                # Reconnect to the newly created database
                return pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database, port=self.port, charset='utf8mb4')
            else:
                raise

    def create_firewall_rules_table(self, connection):
        # SQL command to insert data
        sample_query = """INSERT INTO firewall_rules (IP, AllowDeny, Protocol, Weighting)
                          VALUES (%s, %s, %s, %s)"""
    
        # Data tuple matching the SQL placeholders
        test_samples = ('192.168.1.1', 'Allow', 'TCP', 10)

        try:
            with connection.cursor() as cursor:
                # Create the table if it doesn't exist
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS firewall_rules (
                        RuleID INT AUTO_INCREMENT PRIMARY KEY,
                        IP VARCHAR(15),
                        AllowDeny ENUM('Allow', 'Deny') NOT NULL,
                        Protocol ENUM('TCP', 'UDP', 'ALL') NOT NULL,
                        Weighting INT
                    )
                """)
                connection.commit()

                # Insert data into the table
                cursor.execute(sample_query, test_samples)
                connection.commit()
        except pymysql.Error as e:
            print(f"An error occurred: {e}")



    def connect_and_initialize(self):
        connection = self.connect()
        self.create_firewall_rules_table(connection)
        return connection

if __name__ == "__main__":
    db = DatabaseConnection()
    connection = db.connect_and_initialize()
    print("Database and table setup complete.")

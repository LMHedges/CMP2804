import pymysql

class DatabaseConnection:
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.password = 'password'
        self.database = 'FirewallRules'
        self.port = int('3309')

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
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS firewall_rules (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    rule_name VARCHAR(255) NOT NULL,
                    rule_description TEXT
                )
            """)
            connection.commit()

    def connect_and_initialize(self):
        connection = self.connect()
        self.create_firewall_rules_table(connection)
        return connection

if __name__ == "__main__":
    db = DatabaseConnection()
    connection = db.connect_and_initialize()
    print("Database and table setup complete.")

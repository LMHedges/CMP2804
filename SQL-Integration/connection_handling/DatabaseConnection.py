import os
import mysql.connector
from mysql.connector import Error
from connection_handling.CreateDatabase import CreateTable

class DatabaseConnection:
    def __init__(self):
        # Load database configuration upon initialization
        self.database_config = self.load_database_config()

    def load_database_config(self):
        """Load database credentials from the SQL.env file located in the parent directory."""
        config_path = os.path.join(os.path.dirname(__file__), '..', 'SQL.env')
        config = {}
        try:
            with open(config_path, 'r') as f:
                for line in f:
                    if line.strip() and not line.startswith('#'):
                        key, value = line.strip().split('=')
                        config[key.strip()] = value.strip()
        except IOError as e:
            print(f"An error occurred when trying to read SQL.env: {e}")
            raise
        return config

    def connect(self):
        """Connect to the SQL database using credentials loaded from SQL.env."""
        try:
            connection = mysql.connector.connect(
                host=self.database_config.get('DB_HOST'),
                user=self.database_config.get('DB_USER'),
                password=self.database_config.get('DB_PASSWORD'),
                database=self.database_config.get('DB_DATABASE')
            )
            if connection.is_connected():
                db_info = connection.get_server_info()
                print(f"Successfully connected to MySQL Server version {db_info}")
                return connection
        except Error as e:
            print(f"Error connecting to MySQL database: {e}")
            raise

    def connect_and_initialize(self):
        """Connect to the database and initialize the database schema if necessary."""
        connection = self.connect()
        if connection:
            # Create and initialize the database schema using CreateTable
            table_creator = CreateTable(connection)
            table_creator.create_firewall_rules_table()
            table_creator.close_cursor()
        return connection

    def close_connection(self, connection):
        """Close the database connection."""
        if connection and connection.is_connected():
            connection.close()
            print("MySQL connection is closed")

if __name__ == "__main__":
    # Example usage of the DatabaseConnection class
    db_connection = DatabaseConnection()
    connection = db_connection.connect_and_initialize()

    # Here you would add any operations you want to perform with the connection...

    # Always ensure to close the connection when done
    db_connection.close_connection(connection)

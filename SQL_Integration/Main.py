from dotenv import load_dotenv
import os
import uvicorn
from fastapi import FastAPI
from interface_handling.User_CLI import UserCLI
from connection_handling.DatabaseConnection import DatabaseConnection

# Assumes ModifyTable and other necessary classes are in appropriate modules
from ModifyTable import ModifyTable

# Defines local directory to allow for relative pathing across any device running the code
CurrentDirectory = os.path.dirname(__file__)
RootDirectory = os.path.join(CurrentDirectory, "..")

# Load environment variables from SQL.env
env_path = os.path.join('SQL-Integration', 'SQL.env')
load_dotenv(dotenv_path=env_path)

# Environment variables with default values in case they're not set
StorageType = os.getenv("StorageType", "SQL")  # Default to SQL if not specified
InputUserFormat = os.getenv("InputUserFormat", "User")  # Default to User if not specified

app = FastAPI()  # Initialize FastAPI app here to ensure it's ready for uvicorn

# Setup database connection and cursor
db_connection = DatabaseConnection()
connection = db_connection.connect_and_initialize()
cursor = connection.cursor()

# Initiate classes
ModifyTable_instance = ModifyTable(StorageType, cursor)

if StorageType == "SQL":
    print("SQL chosen")
elif StorageType == "CSV":
    print("CSV chosen")
    CSVFilePath = os.path.join(RootDirectory, "FirewallRules.csv")

# Main function to start the FastAPI server using uvicorn
if __name__ == "__main__":
    if os.getenv("StorageType") == "SQL":
        print("SQL chosen")
        # Specify the correct module path where the FastAPI app is defined
        uvicorn.run("interface_handling.System_API:app", host="127.0.0.1", port=8000, reload=True)



if InputUserFormat == "User":
    user_cli = UserCLI(connection)  # Create instance once
    user_cli.collect_data()  # Prompts user for data input



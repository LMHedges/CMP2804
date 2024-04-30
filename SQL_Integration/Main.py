from dotenv import load_dotenv
import os
import uvicorn
from fastapi import FastAPI
from interface_handling.User_CLI import UserCLI
from connection_handling.DatabaseConnection import DatabaseConnection
from ModifyTable import ModifyTable

# Import FastAPI instances from other modules
from interface_handling.System_API import app as system_api_app
from packet_logging.packet_logging import app as packet_logging_app

# Setup Main FastAPI app
app = FastAPI()

# Mount sub-applications under specific paths
app.mount("/api/system", system_api_app)
app.mount("/api/packet-logging", packet_logging_app)

# Remainder of your main setup should be placed within asynchronous functions

async def startup():
    # Setup database connection and cursor
    db_connection = DatabaseConnection()
    connection = await db_connection.connect_and_initialize_async()
    cursor = connection.cursor()

    # Initiate classes based on environment settings
    ModifyTable_instance = ModifyTable(os.getenv("StorageType", "SQL"), cursor)

    if os.getenv("StorageType") == "SQL":
        print("SQL chosen")
    elif os.getenv("StorageType") == "CSV":
        print("CSV chosen")
        CSVFilePath = os.path.join(RootDirectory, "FirewallRules.csv")

async def user_input():
    if os.getenv("InputUserFormat", "User") == "User":
        user_cli = UserCLI(connection)  # Create instance once
        await user_cli.collect_data_async()  # Prompts user for data input

if __name__ == "__main__":
    # Run the main application asynchronously
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(startup())
    loop.run_until_complete(user_input())

    # Run FastAPI asynchronously
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)

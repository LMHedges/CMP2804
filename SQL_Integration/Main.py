from dotenv import load_dotenv
import os
import uvicorn
from fastapi import FastAPI
import asyncio

from interface_handling.User_CLI import UserCLI
from connection_handling.DatabaseConnection import DatabaseConnection
from ModifyTable import ModifyTable


# Import FastAPI instances from other modules
from interface_handling.System_API import app as system_api_app
from packet_logging.packet_logging import app as packet_logging_app

# Mounts FastAPI points to the new endpoints of /api/system and /api/packet-logging (example url http://127.0.0.1:8000/api/system/docs)
app = FastAPI()
app.mount("/api/system", system_api_app)
app.mount("/api/packet-logging", packet_logging_app)


# Handles startup including user interaction and defines pathways to guide the user depending on their choices
async def startup():
    # Verify valid database connection 
    db_connection = DatabaseConnection()
    connection = await db_connection.connect_and_initialize_async()
    cursor = connection.cursor()
    
    ModifyTable_instance = ModifyTable(os.getenv("StorageType", "SQL"), cursor) # class initiation
    if os.getenv("StorageType") == "SQL":
        print("SQL chosen")


# create a single process to ask the user for an input - will hold the given process until a response it given
async def user_input():
    if os.getenv("InputUserFormat", "User") == "User":
        user_cli = UserCLI(connection)
        await user_cli.collect_data_async()  

# verifies if this is the main file before beginning the async loop
if __name__ == "__main__":
    loop = asyncio.get_event_loop() # retrieves event loop 
    loop.run_until_complete(startup()) # runs the startup function in an async loop (waits for startup to finish before proceeding to user_input())
    loop.run_until_complete(user_input()) # runs user_input function - will hold the given process until a response it given
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True) # opens fastAPI - host can be switched to 0.0.0.0 for blanket open interfaces (less secure) and reloading can be disabled in production

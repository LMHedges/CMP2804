from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import pymysql
from dotenv import load_dotenv
import os

app = FastAPI()

class PacketLog(BaseModel):
    timestamp: datetime
    src_ip: str
    dst_ip: str
    protocol: str
    payload: str

# Load environment settings from SQL.env (uses relative pathing) - ignores the database field and uses packet_logs regardless
env_path = os.path.join(os.path.dirname(__file__), '..', 'SQL.env')
load_dotenv(dotenv_path=env_path)

# Establishes connection to the "packet_logs" database.
# The database is split entirely to allow atomocity as packet logging will likely have a high throughput. Having an entirely seperate database stops unnecessary locks on other tables.
def get_db_connection():
    return pymysql.connect(
        host=os.getenv('SQLHost'),
        user=os.getenv('SQLUser'),
        password=os.getenv('SQLPassword'),
        port=int(os.getenv('SQLPort')),
        database=('packet_logs'), 
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )

# Runs on the startup of fastAPI to create the database and table "packet_logs" if they don't already exist (the table will need to be deleted for columns to be changed)
# The startup and shutdown decorators require fastAPI 0.45.0 or later to be installed, deprication warnings can be ignored.
@app.on_event("startup")
async def startup_event():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("CREATE DATABASE IF NOT EXISTS packet_logs")
            cursor.execute("USE packet_logs")

            # id does not need to be entered as it is auto-incremented. timestamp MUST be injected, ideally before being sent from the client's endpoint
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS packet_logs (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    timestamp DATETIME,
                    src_ip VARCHAR(15),
                    dst_ip VARCHAR(15),
                    protocol VARCHAR(50),
                    payload TEXT
                )
            """)
        conn.commit()
        
    # generic exception handling with error description
    except Exception as exception:
        print(f"Error during database setup: {exception}")
    conn.close() # close the cursor thread


# POST request to add a packet log to the database (see footer for sample query)
@app.post("/packet-logs/", response_model=PacketLog)
def add_packet_log(packet_log: PacketLog):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO packet_logs (timestamp, src_ip, dst_ip, protocol, payload) VALUES (%s, %s, %s, %s, %s)",
                (packet_log.timestamp, packet_log.src_ip, packet_log.dst_ip, packet_log.protocol, packet_log.payload)
            )
        conn.commit()
        return packet_log
    
    # generic catchall exception handling with error description
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    conn.close() # close the cursor thread


# ############ #
# Sample Query #
# ############ #    
# {
#  "timestamp": "2024-04-30T17:03:46.035Z",
#  "src_ip": "1.1.1.1",
#  "dst_ip": "9.9.9.9",
#  "protocol": "TCP",
#  "payload": "ExampleHeaderDetails"
#}
     
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, ValidationError
from typing import Optional
from dotenv import load_dotenv
import pymysql
import os
import sys
import logging
import time

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

from connection_handling.DatabaseConnection import DatabaseConnection

app = FastAPI()
logging.basicConfig(filename='API_logs.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


# Load environment variables
env_path = os.path.join(os.path.dirname(__file__), '..', 'SQL.env')
load_dotenv(dotenv_path=env_path)


class FirewallRule(BaseModel):
    ip: str = Field(..., alias='ip')
    allow_deny: str = Field(..., alias='allow_deny')
    protocol: str = Field(..., alias='protocol')
    weight: Optional[int] = Field(None, alias='weight')
    id: Optional[int] = Field(None, alias='id') 

    class Config:
        allow_population_by_field_name = True
        orm_mode = True
        schema_extra = {
            "example": {
                "ip": "10.11.12.13",
                "allow_deny": "Allow",
                "protocol": "ALL",
                "weight": 5,
                "id": 32
            }
        }
        

# Get database connection from the DatabaseConnection class
db_connection = DatabaseConnection()

# API Endpoints
@app.get("/rules", response_model=list[FirewallRule])
def get_rules():
    db_conn = DatabaseConnection()
    conn = db_conn.connect_and_initialize()
    cursor = conn.cursor()
    cursor.execute("SELECT IP as 'ip', AllowDeny as 'allow_deny', Protocol as 'protocol', Weighting as 'weight' FROM firewall_rules")
    rules = cursor.fetchall()
    conn.close()
    return rules 


@app.post("/rules", response_model=FirewallRule)
def add_rule(rule: FirewallRule):
    with db_connection.connect_and_initialize() as conn:
        cursor = conn.cursor()
        query = "INSERT INTO firewall_rules (IP, AllowDeny, Protocol, Weighting) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (rule.ip, rule.allow_deny, rule.protocol, rule.weight))
        conn.commit()
        rule_id = cursor.lastrowid
    return {**rule.dict(), "id": rule_id}

@app.delete("/rules/{rule_id}", response_model=FirewallRule)
def remove_rule(rule_id: int):
    with db_connection.connect_and_initialize() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM firewall_rules WHERE RuleID = %s", (rule_id,))
        rule = cursor.fetchone()
        if not rule:
            raise HTTPException(status_code=404, detail="Rule not found")
        cursor.execute("DELETE FROM firewall_rules WHERE RuleID = %s", (rule_id,))
        conn.commit()
    return rule

# Running the API with Uvicorn
#if __name__ == "__main__":
#    import uvicorn
#    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)



@app.get("/test-rule")
def test_rule():
    # Simulate database row as a dictionary with correct field names
    simulated_row = {'IP': '192.168.1.1', 'AllowDeny': 'Allow', 'Protocol': 'TCP', 'Weighting': 10}
    
    try:
        # Try to create a FirewallRule instance using the simulated row
        rule = FirewallRule(**simulated_row)
        return rule
    except ValidationError as e:
        # Return the error details if there is a validation error
        return {"error": str(e), "data": simulated_row}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
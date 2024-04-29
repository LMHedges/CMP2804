from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, ValidationError
from typing import Optional
from dotenv import load_dotenv
import pymysql
import os
import sys


root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

from connection_handling.DatabaseConnection import DatabaseConnection

app = FastAPI()

# Load environment variables
env_path = os.path.join(os.path.dirname(__file__), '..', 'SQL.env')
load_dotenv(dotenv_path=env_path)


class FirewallRule(BaseModel):
    ip: str = Field(..., alias='IP')
    allow_deny: str = Field(..., alias='AllowDeny')
    protocol: str = Field(..., alias='Protocol')
    weight: Optional[int] = Field(None, alias='Weighting')

# Get database connection from the DatabaseConnection class
db_connection = DatabaseConnection()

# API Endpoints
@app.get("/rules", response_model=list[FirewallRule])
def get_rules():
    db_conn = DatabaseConnection()
    conn = db_conn.connect_and_initialize()
    with conn.cursor() as cursor:
        cursor.execute("SELECT IP, AllowDeny, Protocol, Weighting FROM firewall_rules")
        rules = cursor.fetchall()
    conn.close()
    rules_models = [FirewallRule(**rule) for rule in rules]
    return rules_models

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
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)



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
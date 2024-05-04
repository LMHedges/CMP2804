import asyncio
import pymysql
import ipaddress
import os
from ModifyTable import ModifyTable
import time

class UserCLI:
    # Iniates class - assumes SQL is being used for data storage.
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.modify_table = ModifyTable("SQL", self.db_connection.cursor())

    # Prompts user for inputs and validates the formatting. Won't allow the user to progress unless a valid input has been provided.
    def collect_data(self):
        time.sleep(1) # Synthetic wait period to slow the information being served to the user to a more readable pace
        ip = self.validate_ip(input("Enter IP address: "))
        allow_deny = self.validate_allow_deny(input("Enter Allow or Deny: "))
        protocol = self.validate_protocol(input("Enter Protocol (TCP/UDP/ALL): "))
        weighting = self.validate_weighting(input("Enter Weighting (integer): "))
        return (ip, allow_deny, protocol, weighting)

    
    # ########################### #
    #    Validation Functions     #
    # ########################### #
    
    # Validate IP
    def validate_ip(self, ip):
        try:
            ipaddress.ip_address(ip)
            return ip
        except ValueError:
            return self.validate_ip(input("Invalid IP address. Please enter a valid IP address: "))

    # Validate Allow/Deny
    def validate_allow_deny(self, allow_deny):
        while allow_deny not in ['Allow', 'Deny']:
            allow_deny = input("Invalid entry. Enter Allow or Deny: ")
        return allow_deny

    # Validate Protocol
    def validate_protocol(self, protocol):
        while protocol not in ['TCP', 'UDP', 'ALL']:
            protocol = input("Invalid entry. Enter Protocol (TCP/UDP/ALL): ")
        return protocol

    # Validate Weighting
    def validate_weighting(self, weighting):
        while not weighting.isdigit():
            weighting = input("Invalid entry. Enter an integer for weighting: ")
        return int(weighting)

    # Inserts data into the ModifyTable object once data has been collected and the user confirms they are happy with the data
    def insert_data(self, data):
        self.modify_table.InsertRow(self.modify_table).insert(*data)

    # Allows users to delete their previouly entered data if they change their mind
    def run(self):
        while True:
            data = self.collect_data()
            self.insert_data(data)
            if input("Continue? (y/n): ").lower() != 'y':
                break

    # Allows asyncronous processing of the collect_data function when being handled from main.py to avoid blocking the main thread
    async def collect_data_async(self):
        return await asyncio.to_thread(self.collect_data)

# Test process to verify database connectivity when running this program independant of database verification in connection_handling/DatabaseConnection.py
if __name__ == "__main__":
    load_dotenv()
    db_connection = pymysql.connect(
        host=os.getenv('SQLHost'),
        user=os.getenv('SQLUser'),
        password=os.getenv('SQLPassword'),
        database=os.getenv('SQLDatabase'),
        port=int(os.getenv('SQLPort')),
        charset='utf8mb4'
    )
    
    cli = UserCLI(db_connection)
    cli.run()
    db_connection.close()

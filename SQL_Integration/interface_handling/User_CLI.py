import asyncio
import pymysql
import ipaddress
import os
from ModifyTable import ModifyTable
import time

class UserCLI:
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.modify_table = ModifyTable("SQL", self.db_connection.cursor())

    def collect_data(self):
        # Collecting user data with validation
        time.sleep(1) # Synthetic wait period to slow the information being served to the user to a more readable pace
        ip = self.validate_ip(input("Enter IP address: "))
        allow_deny = self.validate_allow_deny(input("Enter Allow or Deny: "))
        protocol = self.validate_protocol(input("Enter Protocol (TCP/UDP/ALL): "))
        weighting = self.validate_weighting(input("Enter Weighting (integer): "))
        return (ip, allow_deny, protocol, weighting)

    def validate_ip(self, ip):
        try:
            # Validate the IP address using ipaddress module
            ipaddress.ip_address(ip)
            return ip
        except ValueError:
            # Prompt the user again if the IP is invalid
            return self.validate_ip(input("Invalid IP address. Please enter a valid IP address: "))

    def validate_allow_deny(self, allow_deny):
        # Ensure only 'Allow' or 'Deny' is accepted
        while allow_deny not in ['Allow', 'Deny']:
            allow_deny = input("Invalid entry. Enter Allow or Deny: ")
        return allow_deny

    def validate_protocol(self, protocol):
        # Ensure only 'TCP', 'UDP', or 'ALL' is accepted
        while protocol not in ['TCP', 'UDP', 'ALL']:
            protocol = input("Invalid entry. Enter Protocol (TCP/UDP/ALL): ")
        return protocol

    def validate_weighting(self, weighting):
        # Ensure the weighting is an integer
        while not weighting.isdigit():
            weighting = input("Invalid entry. Enter an integer for weighting: ")
        return int(weighting)

    def insert_data(self, data):
        # Insert data into the database
        self.modify_table.InsertRow(self.modify_table).insert(*data)

    def run(self):
        # Main loop for the CLI
        while True:
            data = self.collect_data()
            self.insert_data(data)
            if input("Continue? (y/n): ").lower() != 'y':
                break

    async def collect_data_async(self):
        # Asynchronously calling collect_data method using asyncio.to_thread
        return await asyncio.to_thread(self.collect_data)

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

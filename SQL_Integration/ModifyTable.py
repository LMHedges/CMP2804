class ModifyTable:
    def __init__(self, StorageType, cursor):
        self.StorageType = StorageType
        self.cursor = cursor
    # Inserts row into the database, currently natively supports SQL but can relatively easily be expanded to support CSV's, Flatfiles, etc
    class InsertRow:
        def __init__(self, parent):
            self.parent = parent

        # Inserts a row via SQL. Requires a pre-existing cursor object to be connected to the database AND validation externally or from the adjacent "insert" class that the .env file is set to SQL
        def InsertRow_db(self, ip, allow_deny, protocol, weighting):
            query = """
                INSERT INTO firewall_rules (IP, AllowDeny, Protocol, Weighting)
                VALUES (%s, %s, %s, %s)
            """
            data = (ip, allow_deny, protocol, weighting)
            self.parent.cursor.execute(query, data)
            self.parent.cursor.connection.commit()

        # Inserts a row in FirewallRules.csv
        def InsertRow_csv(self, IP_Address, Action, Protocol, Weighting):
            import csv
            RuleID = 0

            # Gets the last RuleID in FirewallRules
            with open('FirewallRules.csv', 'r') as file:
                FirewallRules = csv.reader(file)
                RuleID = FirewallRules[-5]
                file.close()

            RuleID+= 1
            data = (RuleID, IP_Address, Action, Protocol, Weighting)

            with open('FirewallRules.csv', 'w') as file: 
                FirewallRules = csv.writer(file)
                FirewallRules.writerow(data)
                file.close()

        def insert(self, ip, allow_deny, protocol, weighting):
            if self.parent.StorageType == "SQL":
                self.InsertRow_db(ip, allow_deny, protocol, weighting)
            else:
                self.InsertRow_csv(ip, allow_deny, protocol, weighting)


    # Outputs all the IP addresses in the firewall_rules .csv and .db
    class OutputIP:
        def __init__(self, parent):
            self.parent = parent
           
        def OutputIP_db(self):
            query = """
                SELECT IP_Address FROM firewall_rules
            """
            self.parent.cursor.execute(query)
            IP_List = self.parent.cursor.fetchall()
            return IP_List
        
        def OutputIP_csv(self):
            file = open('FirewallRules.csv', 'r')
            IP_List = []
            for col in file:
                IP_List.append(col['IP_Address'])
            file.close()
            return IP_List
        
        def Output(self):
            if self.parent.StorageType == "SQL":
                self.OutputIP_db()
            else:
                self.OutputIP_csv()
        
    # Removes a row based off IP address from the firewall_rules .csv and .db
    class RemoveRow:
        def __init__(self, parent):
            self.parent = parent

        def RemoveRow_db(self, ip):
            query = """
                DELETE FROM firewall_rules
                WHERE IP_Address = %s
            """
            self.parent.cursor.execute(query, ip)
            self.parent.cursor.connection.commit()

        def RemoveRow_csv(self, ip):
            import csv
            entries = []
            with open('FirewallRules.csv', 'r') as file:
                FirewallRules = csv.reader(file)
                for row in FirewallRules:
                    for field in entries:
                        if field == ip:
                            entries.remove(row)
                file.close()
            with open('FirewallRules.csv', 'w') as file:
                FirewallRules = csv.writer(file)
                FirewallRules.writerows(entries)

        def Remove(self, ip):
            if self.parent.StorageType == "SQL":
                self.RemoveRow_db(ip)
            else:
                self.RemoveRow_csv(ip)

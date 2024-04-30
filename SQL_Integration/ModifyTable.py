class ModifyTable:
    def __init__(self, StorageType, cursor):
        self.StorageType = StorageType
        self.cursor = cursor

    class InsertRow:
        def __init__(self, parent):
            self.parent = parent

        def InsertRowSQL(self, ip, allow_deny, protocol, weighting):
            # Use a parameterized query to safely insert data
            query = """
                INSERT INTO firewall_rules (IP, AllowDeny, Protocol, Weighting)
                VALUES (%s, %s, %s, %s)
            """
            data = (ip, allow_deny, protocol, weighting)
            self.parent.cursor.execute(query, data)
            self.parent.cursor.connection.commit()

        def insert(self, ip, allow_deny, protocol, weighting):
            if self.parent.StorageType == "SQL":
                self.InsertRowSQL(ip, allow_deny, protocol, weighting)
            else:
                # Add handling for CSV or other storage types if necessary
                pass

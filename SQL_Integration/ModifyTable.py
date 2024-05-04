class ModifyTable:
    def __init__(self, StorageType, cursor):
        self.StorageType = StorageType
        self.cursor = cursor

    # Inserts row into the database, currently natively supports SQL but can relatively easily be expanded to support CSV's, Flatfiles, etc
    class InsertRow:
        def __init__(self, parent):
            self.parent = parent

        # Inserts a row via SQL. Requires a pre-existing cursor object to be connected to the database AND validation externally or from the adjacent "insert" class that the .env file is set to SQL
        def InsertRowSQL(self, ip, allow_deny, protocol, weighting):
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
                # Placeholder for CSV/other formats. Not able to proceed without code from others.
                pass

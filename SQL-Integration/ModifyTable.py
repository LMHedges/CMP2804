class ModifyTable:
    def __init__(self, StorageType, cursor):
        self.StorageType = StorageType
        self.cursor = cursor  # Cursor passed from DatabaseConnection

    #######################################
    ##         "insert" handling         ##
    #######################################
    class InsertRow:
        # Initiates class with parent
        def __init__(self, parent):
            self.parent = parent

        # Inserts the newly made rule into an SQL database using the existing cursor
        def InsertRowSQL(self, Query):
            self.parent.cursor.execute("INSERT INTO FirewallRules SET " + Query)
            self.parent.cursor.connection.commit()

        # Inserts the newly made rule into a CSV file (assuming StorageType is set to CSV)
        def InsertRowCSV(self, Query):
            # Implementation would be required here for CSV file manipulation
            pass

        def insert(self, Query):
            if self.parent.StorageType == "SQL":
                self.InsertRowSQL(Query)
            elif self.parent.StorageType == "CSV":
                self.InsertRowCSV(Query)

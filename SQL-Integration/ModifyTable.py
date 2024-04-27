class ModifyTable:
    def __init__(self, StorageType):
        self.StorageType = StorageType

    class InsertRow:
        def __init__(self, parent):
            self.parent = parent       

        def insert(self, Query):
            
            if self.parent.StorageType == "SQL":
                self.InsertRowCSV(Query)
            
            elif self.parent.StorageType == "CSV":
                self.InsertRowCSV(Query)

        def InsertRowSQL(self, Query):
            cursor.execute("INSERT INTO rulesetdatabase ", Query, " ;")

        def InsertRowCSV(self, Query):
            pass
        

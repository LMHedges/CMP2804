class ModifyTable:
    def __init__(self, StorageType):
        self.StorageType = StorageType
        
    


    #######################################
    ##         "insert" handling         ##
    #######################################
    class InsertRow:
        # Initiates class with parent
        def __init__(self, parent):
            self.parent = parent       
            
        # Inserts the newly made rule into an SQL database (assuming environmental variable is set)
        def InsertRowSQL(self, Query):
            cursor.execute("INSERT INTO rulesetdatabase ", Query, " ;")

        # Inserts the newly made rule into a CSV file (requires environmental variable to be set to CSV)
        def InsertRowCSV(self, Query):
            pass


        def insert(self, Query):
            if self.parent.StorageType == "SQL":
                self.InsertRowCSV(Query)
            
            elif self.parent.StorageType == "CSV":
                self.InsertRowCSV(Query)



        
        

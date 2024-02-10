class ModifyTable:
    def __init__(self, StorageType):
        self.StorageType = StorageType

    class InsertRow:
        def __init__(self, parent):
            self.parent = parent       

        def insert(self, ExampleQuery):
            
            if self.parent.StorageType == "SQL":
                self.InsertRowCSV(ExampleQuery)
            
            elif self.parent.StorageType == "CSV":
                self.InsertRowCSV(ExampleQuery)

        def InsertRowSQL(self, ExampleQuery):
            pass

        def InsertRowCSV(self, ExampleQuery):
            pass
        

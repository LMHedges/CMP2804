## ############################ ## 
## reading from table data ONLY ## 
## ############################ ## 


class ReadData:
    
    # Loads csv table into primary memory allowing quick read access
    def OpenCSV(CSVFilePath):
        print("CSV Format File Storage has been selected")
        with open('FirewallRules.csv', 'r') as CSVFilePath:
            TableData = csv.reader(CSVFilePath)
            for record in TableData:
                print(record)
         

    # Validates if SQL credentials are valid
    def CheckSQLConnection():
        print("SQL Storage has been selected")
        try:
            mydb = mysql.connector.connect(
                host = os.getenv("SQLHost"),
                port = os.getenv("SQLPort"),
                user = os.getenv("SQLUser"),
                passwd = os.getenv("SQLPassword"),
                database = os.getenv("rulesetdatabase")
            )
            print("Valid SQL connection credentials provided")
       
            CreateDatabaseIfNotExists() # Creates a table for the firewall rules if it doesn't already exist
            return True
        except:
            print("Valid SQL connection credentials NOT provided")
            return False
        
    # Reads from SQL table and prints all records
    def ReadSQLTable():
        print("Reading from SQL Table...")
        try:
            # Establish a new connection using environment variables
            mydb = mysql.connector.connect(
                host=os.getenv("SQLHost"),
                port=os.getenv("SQLPort"),
                user=os.getenv("SQLUser"),
                passwd=os.getenv("SQLPassword"),
                database=os.getenv("rulesetdatabase")  # Ensure this is the correct env variable for the database name
            )
            cursor = mydb.cursor()

            # Execute SQL query to fetch all records from FirewallRules
            cursor.execute("USE rulesetdatabase")
            cursor.execute("SELECT * FROM FirewallRules")

            # Fetch all rows from the last executed query
            records = cursor.fetchall()

            # Check if there are records to print, otherwise state it's empty
            if records:
                print("Displaying all records from FirewallRules:")
                for record in records:
                    print(record)
            else:
                print("No records found in FirewallRules.")

            # Close the cursor and connection
            cursor.close()
            mydb.close()

        except mysql.connector.Error as err:
            print(f"Error reading from MySQL table: {err}")
    


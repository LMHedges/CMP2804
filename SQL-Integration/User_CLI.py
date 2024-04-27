import time

def run_user_cli():
    # Check if the necessary environment variable is set
    import os
    InputUserFormat = os.getenv("InputUserFormat", "default")

    if InputUserFormat == "User":
        print("What would you like to do? \n")
        choice = input("")
        if choice == "exit":
            print("Goodbye")
            time.sleep(1)
            exit()

        elif choice == "insert":
            QueryField = []
            print("Please enter the following details: \n")
            QueryField.append(input("IP Address: "))
            QueryField.append(input("Action (Allow/Deny/Bypass): "))
            QueryField.append(input("Protocol (TCP/UDP/ALL): "))
            QueryField.append(input("Weighting: "))

        elif choice == "delete":
            pass
        elif choice == "update":
            pass

    elif InputUserFormat == "api":
        pass

    else:
        print("Invalid InputUserFormat environmental variable")
        exit()

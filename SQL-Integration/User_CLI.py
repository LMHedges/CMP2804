import time
import os
from Validation import Validation # used for IP address, action, protocol, weighting validation 

def get_valid_input(prompt, validation_function):
    """Prompt the user for input and validate the input using the provided function."""
    while True:
        user_input = input(prompt)
        if validation_function(user_input):
            return user_input
        else:
            print("Invalid input, please try again.")

def run_user_cli(InputUserFormat, StorageType):

    if InputUserFormat == "User":
        print("What would you like to do? \n")
        choice = input("")
        if choice == "exit":
            print("Goodbye")
            time.sleep(1)
            exit()

        elif choice == "insert":
            print("Please enter the following details: \n")
            QueryField = []
            # Validate IP address
            ip_address = get_valid_input("IP Address: ", Validation.check_ip_address)
            QueryField.append(ip_address)

            # Validate action
            action = get_valid_input("Action (Allow/Deny/Bypass): ", Validation.check_action)
            QueryField.append(action)

            # Validate protocol
            protocol = get_valid_input("Protocol (TCP/UDP/ALL): ", Validation.check_protocol)
            QueryField.append(protocol)

            # Validate weighting
            weighting = get_valid_input("Weighting: ", Validation.check_weighting)
            QueryField.append(weighting)

            print("Data entered successfully:", QueryField)

        elif choice == "delete":
            pass
        elif choice == "update":
            pass

    # Theoretically impossible as the function is only called IF the environmental variable is set to "User" but acts as a further check
    elif InputUserFormat == "api":
        pass

    else:
        print("Invalid InputUserFormat environmental variable")
        exit()

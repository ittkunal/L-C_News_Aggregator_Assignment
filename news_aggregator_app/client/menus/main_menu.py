import sys
from client.services.auth_service import login, signup

def show_main_menu():
    while True:
        try:
            print("Welcome to the News Aggregator application. Please choose the options below.")
            print("1. Login")
            print("2. Sign up")
            print("3. Exit")
            choice = input("Enter your choice: ")
            if choice == "1":
                login()
            elif choice == "2":
                signup()
            elif choice == "3":
                print("Goodbye!")
                sys.exit(0)
            else:
                print("Invalid choice. Try again.")
        except KeyboardInterrupt:
            print("\n\nGoodbye! Application terminated gracefully.")
            sys.exit(0)
        except EOFError:
            print("\n\nGoodbye! Application terminated gracefully.")
            sys.exit(0)
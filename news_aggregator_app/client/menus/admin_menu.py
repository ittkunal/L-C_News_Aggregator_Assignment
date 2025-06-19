from client.services.admin_service import (
    view_sources, view_source_details, update_source, add_category
)

def show_admin_menu():
    while True:
        print("\nAdmin Menu:")
        print("1. View the list of external servers and status")
        print("2. View the external server’s details")
        print("3. Update/Edit the external server’s details")
        print("4. Add new News Category")
        print("5. Logout")
        choice = input("Enter your choice: ")
        if choice == "1":
            view_sources()
        elif choice == "2":
            view_source_details()
        elif choice == "3":
            update_source()
        elif choice == "4":
            add_category()
        elif choice == "5":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Try again.")
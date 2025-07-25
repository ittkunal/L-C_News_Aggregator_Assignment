from client.services.admin_service import (
    view_sources,
    view_source_details,
    update_source,
    add_category,
    view_reported_articles,
    hide_unhide_article,
    hide_unhide_category,
    manage_filtered_keywords
)

def show_admin_menu():
    while True:
        print("1. View the list of external servers and status")
        print("2. View the external server’s details")
        print("3. Update/Edit the external server’s details")
        print("4. Add new News Category")
        print("5. View Reported Articles")
        print("6. Hide/Unhide Article")
        print("7. Hide/Unhide Category")
        print("8. Manage Filtered Keywords")
        print("9. Logout")
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
            view_reported_articles()
        elif choice == "6":
            hide_unhide_article()
        elif choice == "7":
            hide_unhide_category()
        elif choice == "8":
            manage_filtered_keywords()
        elif choice == "9":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Try again.")

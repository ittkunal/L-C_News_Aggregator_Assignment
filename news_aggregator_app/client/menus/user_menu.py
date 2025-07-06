from client.utils.session_store import get_session
from datetime import datetime
from client.services.user_service import (
    show_headlines_menu, show_saved_articles_menu, search_articles, show_notifications_menu, report_article
)

def show_user_menu():
    session = get_session()
    username = session.get("username", "User")  
    while True:
        now = datetime.now()
        date_str = now.strftime("%d-%b-%Y")
        time_str = now.strftime("%I:%M%p")
        print(f"\nWelcome to the News Application, {username}! Date: {date_str} \nTime:{time_str}")
        print("Please choose the options below")
        print("1. Headlines")
        print("2. Saved Articles")
        print("3. Search")
        print("4. Notifications")
        print("5. Report Article")
        print("6. Logout")
        choice = input("Enter your choice: ")
        if choice == "1":
            show_headlines_menu()
        elif choice == "2":
            show_saved_articles_menu()
        elif choice == "3":
            search_articles()
        elif choice == "4":
            show_notifications_menu()
        elif choice == "5":
            report_article()
        elif choice == "6":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Try again.")
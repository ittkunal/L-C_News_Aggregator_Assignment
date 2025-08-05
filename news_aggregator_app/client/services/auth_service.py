import sys
import requests
from client.utils.session_store import set_session
from client.menus.admin_menu import show_admin_menu
from client.menus.user_menu import show_user_menu
from getpass import getpass
import re

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

API_URL = "http://localhost:8000/auth"

def login():
    try:
        username = input("Username: ")
        password = getpass("Password: ")
        resp = requests.post(f"{API_URL}/login", json={"username": username, "password": password})
        if resp.status_code == 200:
            data = resp.json()
            set_session(data["user_id"], data["is_admin"], data.get("username"))
            print("Login successful!")
            if data["is_admin"]:
                show_admin_menu()
            else:
                show_user_menu()
        else:
            try:
                error = resp.json()
                if isinstance(error.get("detail"), list):
                    for err in error["detail"]:
                        print(f"Login failed: {err.get('msg')}")
                else:
                    print("Login failed:", error.get("detail"))
            except Exception:
                print("Login failed: Unknown error.")
    except KeyboardInterrupt:
        print("\n\nGoodbye! Application terminated gracefully.")
        sys.exit(0)
    except EOFError:
        print("\n\nGoodbye! Application terminated gracefully.")
        sys.exit(0)

def signup():
    try:
        username = input("Username: ")
        email = input("Email: ")
        if not is_valid_email(email):
            print("Invalid email address. Please try again.")
            return
        password = getpass("Password: ")
        resp = requests.post(f"{API_URL}/signup", json={"username": username, "email": email, "password": password})
        if resp.status_code == 200:
            print("Signup successful! Please login.")
        else:
            print("Signup failed:", resp.json().get("detail"))
    except KeyboardInterrupt:
        print("\n\nGoodbye! Application terminated gracefully.")
        sys.exit(0)
    except EOFError:
        print("\n\nGoodbye! Application terminated gracefully.")
        sys.exit(0)
import requests
from client.utils.session_store import set_session
from client.menus.admin_menu import show_admin_menu
from client.menus.user_menu import show_user_menu

API_URL = "http://localhost:8000/auth"

def login():
    username = input("Username: ")
    password = input("Password: ")
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
            # Handle validation errors (422) which return a list in 'detail'
            if isinstance(error.get("detail"), list):
                for err in error["detail"]:
                    print(f"Login failed: {err.get('msg')}")
            else:
                print("Login failed:", error.get("detail"))
        except Exception:
            print("Login failed: Unknown error.")

def signup():
    username = input("Username: ")
    email = input("Email: ")
    password = input("Password: ")
    resp = requests.post(f"{API_URL}/signup", json={"username": username, "email": email, "password": password})
    if resp.status_code == 200:
        print("Signup successful! Please login.")
    else:
        print("Signup failed:", resp.json().get("detail"))
import requests
from client.utils.session_store import get_session

API_URL = "http://localhost:8000"

def show_headlines_menu():
    session = get_session()
    user_id = session.get("user_id")
    while True:
        print("\nHeadlines Menu:")
        print("1. Today")
        print("2. Date range")
        print("3. Logout")
        choice = input("Enter your choice: ")
        if choice == "1":
            from datetime import datetime
            today = datetime.now().strftime("%Y-%m-%d")
            category = select_category()
            if category is None:
                continue 
            params = {"start": today, "end": today}
            if category != "all":
                params["category"] = category
            resp = requests.get(f"{API_URL}/news/headlines", params=params)
            articles = resp.json()
            display_articles(articles, user_id)
        elif choice == "2":
            start = input("Start date (YYYY-MM-DD): ")
            end = input("End date (YYYY-MM-DD): ")
            category = select_category()
            if category is None:
                continue 
            params = {"start": start, "end": end}
            if category != "all":
                params["category"] = category
            resp = requests.get(f"{API_URL}/news/headlines", params=params)
            articles = resp.json()
            display_articles(articles, user_id)
        elif choice == "3":
            return
        else:
            print("Invalid choice. Try again.")

def select_category():
    print("\nPlease choose the options below for Headlines")
    print("1. All")
    print("2. Business")
    print("3. Entertainment")
    print("4. Sports")
    print("5. Technology")
    print("6. Back")
    category_map = {
        "1": "all",
        "2": "business",
        "3": "entertainment",
        "4": "sports",
        "5": "technology",
        "6": None
    }
    choice = input("Enter your choice: ")
    return category_map.get(choice, "all")

def display_articles(articles, user_id):
    if not articles:
        print("No headlines found for the selected criteria.")
        return
    for art in articles:
        print("\nH E A D L I N E S")
        print(f"Article Id: {art['id']}")
        print(f"{art['title']}")
        if art.get('content'):
            print(f"{art['content'][:100]}...")
        print(f"source: {art['source']}")
        print(f"URL: {art['url']}")
        print(f"Category: {art['category']}")
        print("-" * 40)
    while True:
        print("1. Back")
        print("2. Logout")
        print("3. Save Article")
        sub_choice = input("Enter your choice: ")
        if sub_choice == "1":
            break
        elif sub_choice == "2":
            exit(0)
        elif sub_choice == "3":
            article_id = input("Enter Article ID to save: ")
            resp = requests.post(f"{API_URL}/user/saved-articles", params={"user_id": user_id, "article_id": article_id})
            print(resp.json().get("message", "Failed to save."))
        else:
            print("Invalid choice. Try again.")

def show_saved_articles_menu():
    session = get_session()
    user_id = session.get("user_id")
    resp = requests.get(f"{API_URL}/user/saved-articles", params={"user_id": user_id})
    articles = resp.json()
    if not articles:
        print("No saved articles found.")
    else:
        print("\nS A V E D")
        for art in articles:
            print(f"Article Id: {art['id']} {art['title']}")
            if art.get('content'):
                print(f"{art['content'][:100]}...")
            print(f"source: {art['source']}")
            print(f"URL: {art['url']}")
            print(f"Category: {art['category']}")
            print("-" * 40)
    print("1. Delete Article")
    print("2. Back")
    choice = input("Enter your choice: ")
    if choice == "1":
        article_id = input("Enter Article ID to delete: ")
        resp = requests.delete(f"{API_URL}/user/saved-articles/{article_id}", params={"user_id": user_id})
        print(resp.json().get("message", "Failed to delete."))

def search_articles():
    q = input("Enter search query: ")
    resp = requests.get(f"{API_URL}/news/search", params={"q": q})
    articles = resp.json()
    if not articles:
        print("No articles found for your search.")
    else:
        print("\nS E A R C H")
        for art in articles:
            print(f"Article Id: {art['id']} {art['title']}")
            if art.get('content'):
                print(f"{art['content'][:100]}...")
            print(f"source: {art['source']}")
            print(f"URL: {art['url']}")
            print(f"Category: {art['category']}")
            print("-" * 40)
    print("1. Save Article")
    print("2. Like Article")
    print("3. Dislike Article")
    print("4. Back")
    choice = input("Enter your choice: ")
    if choice == "1":
        article_id = input("Enter Article ID to save: ")
        session = get_session()
        user_id = session.get("user_id")
        resp = requests.post(f"{API_URL}/user/saved-articles", params={"user_id": user_id, "article_id": article_id})
        print(resp.json().get("message", "Failed to save."))
    elif choice == "2":
        article_id = input("Enter Article ID to like: ")
        session = get_session()
        user_id = session.get("user_id")
        resp = requests.post(f"{API_URL}/news/{article_id}/like", params={"user_id": user_id})
        print(resp.json().get("message", "Failed to like."))
    elif choice == "3":
        article_id = input("Enter Article ID to dislike: ")
        session = get_session()
        user_id = session.get("user_id")
        resp = requests.post(f"{API_URL}/news/{article_id}/dislike", params={"user_id": user_id})
        print(resp.json().get("message", "Failed to dislike."))

def show_notifications_menu():
    session = get_session()
    user_id = session.get("user_id")
    while True:
        print("\nN O T I F I C A T I O N S")
        print("1. View Notifications")
        print("2. Configure Notifications")
        print("3. Back")
        print("4. Logout")
        choice = input("Enter your choice: ")
        if choice == "1":
            resp = requests.get(f"{API_URL}/user/notifications", params={"user_id": user_id})
            notifications = resp.json()
            if not notifications:
                print("No notification settings found.")
            else:
                print("\nYour notification settings:")
                for n in notifications:
                    if n['type'] == 'keywords':
                        print(f"Keywords: {n['keywords']}")
                    else:
                        print(f"{n['type'].capitalize()}: {'Enabled' if n['enabled'] else 'Disabled'}")
        elif choice == "2":
            configure_notifications(user_id)
        elif choice == "3":
            break
        elif choice == "4":
            exit(0)
        else:
            print("Invalid choice. Try again.")

def configure_notifications(user_id):
    resp = requests.get(f"{API_URL}/user/notifications", params={"user_id": user_id})
    notifications = resp.json()
    categories = ['business', 'entertainment', 'sports', 'technology']
    notif_dict = {n['type']: n for n in notifications}
    while True:
        print("\nC O N F I G U R E - N O T I F I C A T I O N S")
        for idx, cat in enumerate(categories, 1):
            enabled = notif_dict.get(cat, {}).get('enabled', False)
            keywords = notif_dict.get(cat, {}).get('keywords', '')
            if enabled:
                print(f"{idx}. {cat.capitalize()} - Enabled (keywords: {keywords})")
            else:
                print(f"{idx}. {cat.capitalize()} - Disabled")
        print("5. Back")
        print("6. Logout")
        choice = input("Enter your option: ")
        if choice in ["1", "2", "3", "4"]:
            cat = categories[int(choice)-1]
            current = notif_dict.get(cat, {}).get('enabled', False)
            keywords = notif_dict.get(cat, {}).get('keywords', '')
            while True:
                print(f"\n{cat.capitalize()} is currently {'Enabled' if current else 'Disabled'}.")
                if current:
                    print("1. Disable notifications")
                    print(f"2. Edit keywords for {cat.capitalize()} (current: {keywords})")
                    print("3. Back")
                    sub_choice = input("Enter your choice: ")
                    if sub_choice == "1":
                        resp = requests.put(
                            f"{API_URL}/user/notifications",
                            params={"user_id": user_id, "type": cat, "enabled": False}
                        )
                        print(resp.json().get("message", "Failed to update."))
                        notif_dict[cat] = {"type": cat, "enabled": False, "keywords": keywords}
                        break
                    elif sub_choice == "2":
                        new_keywords = input(f"Enter new keywords for {cat.capitalize()} (comma separated): ")
                        resp = requests.put(
                            f"{API_URL}/user/notifications",
                            params={"user_id": user_id, "type": cat, "enabled": True, "keywords": new_keywords}
                        )
                        print(resp.json().get("message", "Failed to update."))
                        notif_dict[cat] = {"type": cat, "enabled": True, "keywords": new_keywords}
                        break
                    elif sub_choice == "3":
                        break
                    else:
                        print("Invalid choice. Try again.")
                else:
                    print("1. Enable notifications")
                    print("2. Back")
                    sub_choice = input("Enter your choice: ")
                    if sub_choice == "1":
                        new_keywords = input(f"Enter keywords for {cat.capitalize()} (comma separated): ")
                        resp = requests.put(
                            f"{API_URL}/user/notifications",
                            params={"user_id": user_id, "type": cat, "enabled": True, "keywords": new_keywords}
                        )
                        print(resp.json().get("message", "Failed to update."))
                        notif_dict[cat] = {"type": cat, "enabled": True, "keywords": new_keywords}
                        break
                    elif sub_choice == "2":
                        break
                    else:
                        print("Invalid choice. Try again.")
        elif choice == "5":
            break
        elif choice == "6":
            exit(0)
        else:
            print("Invalid choice. Try again.")
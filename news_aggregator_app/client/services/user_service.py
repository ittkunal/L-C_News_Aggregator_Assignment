import requests
from client.utils.session_store import get_session
from datetime import datetime, timedelta

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
            yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
            params = {"start": yesterday, "end": yesterday}
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
    resp = requests.get(f"{API_URL}/news/categories")
    categories = resp.json()
    if not categories:
        print("No categories found.")
        return None
    print("\nPlease choose the options below for Headlines")
    print("0. All")
    for idx, cat in enumerate(categories, 1):
        print(f"{idx}. {cat['name'].capitalize()}")
    print(f"{len(categories)+1}. Back")
    choice = input("Enter your choice: ")
    if choice == "0":
        return "all"
    elif choice == str(len(categories) + 1):
        return None
    else:
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(categories):
                return categories[idx]["name"]
        except:
            pass
    print("Invalid choice. Try again.")
    return select_category()


def display_articles(articles, user_id):
    if not articles:
        print("No headlines found for the selected criteria.")
        return
    for art in articles:
        print("\nH E A D L I N E S")
        print(f"Article Id: {art['id']}")
        print(f"{art['title']}")
        if art.get("content"):
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
            resp = requests.post(
                f"{API_URL}/user/saved-articles",
                params={"user_id": user_id, "article_id": article_id},
            )
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
            if art.get("content"):
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
        resp = requests.delete(
            f"{API_URL}/user/saved-articles/{article_id}", params={"user_id": user_id}
        )
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
            if art.get("content"):
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
        resp = requests.post(
            f"{API_URL}/user/saved-articles",
            params={"user_id": user_id, "article_id": article_id},
        )
        print(resp.json().get("message", "Failed to save."))
    elif choice == "2":
        article_id = input("Enter Article ID to like: ")
        session = get_session()
        user_id = session.get("user_id")
        resp = requests.post(
            f"{API_URL}/news/{article_id}/like", params={"user_id": user_id}
        )
        print(resp.json().get("message", "Failed to like."))
    elif choice == "3":
        article_id = input("Enter Article ID to dislike: ")
        session = get_session()
        user_id = session.get("user_id")
        resp = requests.post(
            f"{API_URL}/news/{article_id}/dislike", params={"user_id": user_id}
        )
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
            cat_resp = requests.get(f"{API_URL}/news/categories")
            categories = cat_resp.json()
            resp = requests.get(
                f"{API_URL}/user/notifications", params={"user_id": user_id}
            )
            notifications = resp.json()
            notif_dict = {n["type"]: n for n in notifications}
            if not categories:
                print("No categories found.")
            else:
                print("\nYour notification settings:")
                for cat in categories:
                    enabled = notif_dict.get(cat["name"], {}).get("enabled", False)
                    if isinstance(enabled, int):
                        enabled = enabled == 1
                    print(
                        f"{cat['name'].capitalize()}: {'Enabled' if enabled else 'Disabled'}"
                    )
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
    cat_resp = requests.get(f"{API_URL}/news/categories")
    categories = cat_resp.json()
    notif_dict = {n["type"]: n for n in notifications}
    while True:
        print("\nC O N F I G U R E - N O T I F I C A T I O N S")
        for idx, cat in enumerate(categories, 1):
            enabled = notif_dict.get(cat["name"], {}).get("enabled", False)
            if isinstance(enabled, int):
                enabled = enabled == 1
            keywords = notif_dict.get(cat["name"], {}).get("keywords", "")
            if enabled:
                print(
                    f"{idx}. {cat['name'].capitalize()} - Enabled (keywords: {keywords})"
                )
            else:
                print(f"{idx}. {cat['name'].capitalize()} - Disabled")
        print(f"{len(categories)+1}. Back")
        print(f"{len(categories)+2}. Logout")
        choice = input("Enter your option: ")
        if choice.isdigit() and 1 <= int(choice) <= len(categories):
            cat_name = categories[int(choice) - 1]["name"]
            current = notif_dict.get(cat_name, {}).get("enabled", False)
            keywords = notif_dict.get(cat_name, {}).get("keywords", "")
            while True:
                print(
                    f"\n{cat_name.capitalize()} is currently {'Enabled' if current else 'Disabled'}."
                )
                if current:
                    print("1. Disable notifications")
                    print(
                        f"2. Edit keywords for {cat_name.capitalize()} (current: {keywords})"
                    )
                    print("3. Back")
                    sub_choice = input("Enter your choice: ")
                    if sub_choice == "1":
                        resp = requests.put(
                            f"{API_URL}/user/notifications",
                            params={
                                "user_id": user_id,
                                "type": cat_name,
                                "enabled": False,
                            },
                        )
                        try:
                            print(resp.json().get("message", "Failed to update."))
                        except Exception:
                            print("Failed to update notification settings. Server response:", resp.text)
                        notif_dict[cat_name] = {
                            "type": cat_name,
                            "enabled": False,
                            "keywords": keywords,
                        }
                        break
                    elif sub_choice == "2":
                        new_keywords = input(
                            f"Enter new keywords for {cat_name.capitalize()} (comma separated): "
                        )
                        resp = requests.put(
                            f"{API_URL}/user/notifications",
                            params={
                                "user_id": user_id,
                                "type": cat_name,
                                "enabled": True,
                                "keywords": new_keywords,
                            },
                        )
                        print(resp.json().get("message", "Failed to update."))
                        notif_dict[cat_name] = {
                            "type": cat_name,
                            "enabled": True,
                            "keywords": new_keywords,
                        }
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
                        new_keywords = input(
                            f"Enter keywords for {cat_name.capitalize()} (comma separated): "
                        )
                        resp = requests.put(
                            f"{API_URL}/user/notifications",
                            params={
                                "user_id": user_id,
                                "type": cat_name,
                                "enabled": True,
                                "keywords": new_keywords,
                            },
                        )
                        print(resp.json().get("message", "Failed to update."))
                        notif_dict[cat_name] = {
                            "type": cat_name,
                            "enabled": True,
                            "keywords": new_keywords,
                        }
                        break
                    elif sub_choice == "2":
                        break
                    else:
                        print("Invalid choice. Try again.")
        elif choice == str(len(categories) + 1):
            break
        elif choice == str(len(categories) + 2):
            exit(0)
        else:
            print("Invalid choice. Try again.")


def report_article():
    session = get_session()
    user_id = session.get("user_id")
    article_id = input("Enter Article ID to report: ")
    reason = input("Reason for reporting: ")
    resp = requests.post(
        f"http://localhost:8000/user/report-article",
        json={"article_id": article_id, "user_id": user_id, "reason": reason},
    )
    if resp.status_code == 200:
        print("Thank you for your feedback. The admin will review this article.")
    else:
        print("Failed to report article:", resp.json().get("detail", "Unknown error"))

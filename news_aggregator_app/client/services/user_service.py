import sys
import requests
import re
from client.utils.session_store import get_session
from datetime import datetime, timedelta

API_URL = "http://localhost:8000"


def is_valid_date_format(date_string):
    if not date_string or not date_string.strip():
        return False
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    if not re.match(pattern, date_string.strip()):
        return False
    try:
        datetime.strptime(date_string.strip(), '%Y-%m-%d')
        return True
    except ValueError:
        return False

def is_valid_date_range(start_date, end_date):
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        if start > end:
            return False
        today = datetime.now().date()
        if start.date() > today or end.date() > today:
            return False
        five_years_ago = datetime.now().date() - timedelta(days=5*365)
        if start.date() < five_years_ago or end.date() < five_years_ago:
            return False
        return True
    except ValueError:
        return False

def show_headlines_menu():
    session = get_session()
    user_id = session.get("user_id")
    while True:
        print("\nHeadlines Menu:")
        print("1. Today")
        print("2. Date range")
        print("3. Back")
        choice = input("Enter your choice: ")
        if choice == "1":
            today = datetime.now().strftime("%Y-%m-%d")
            params = {"start": today, "end": today, "limit": 20}
            resp = requests.get(f"{API_URL}/news/headlines", params=params)
            articles = resp.json()
            display_articles_with_refresh(articles, user_id, "today", params)
        elif choice == "2":
            try:
                start = input("Start date (YYYY-MM-DD): ")
                if not is_valid_date_format(start):
                    print("Invalid start date format. Please use YYYY-MM-DD")
                    continue
                end = input("End date (YYYY-MM-DD): ")
                if not is_valid_date_format(end):
                    print("Invalid end date format. Please use YYYY-MM-DD")
                    continue
                if not is_valid_date_range(start.strip(), end.strip()):
                    print("Invalid date range. Please ensure:")
                    print("  - Start date is before or equal to end date")
                    print("  - Dates are not in the future")
                    print("  - Dates are not older than 5 years")
                    continue
                category = select_category()
                if category is None:
                    continue
                params = {"start": start.strip(), "end": end.strip()}
                if category != "all":
                    params["category"] = category
                resp = requests.get(f"{API_URL}/news/headlines", params=params)
                articles = resp.json()
                display_articles_with_refresh(articles, user_id, "date_range", params)
            except KeyboardInterrupt:
                print("\n\nGoodbye! Application terminated gracefully.")
                sys.exit(0)
            except EOFError:
                print("\n\nGoodbye! Application terminated gracefully.")
                sys.exit(0)
        elif choice == "3":
            return
        else:
            print("Invalid choice. Try again.")

def select_category():
    try:
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
    except KeyboardInterrupt:
        print("\n\nGoodbye! Application terminated gracefully.")
        sys.exit(0)
    except EOFError:
        print("\n\nGoodbye! Application terminated gracefully.")
        sys.exit(0)

def display_articles_with_refresh(articles, user_id, view_type, params=None):
    if not articles:
        print("No headlines found for the selected criteria.")
        return
    while True:
        sorted_articles = sorted(articles, key=lambda x: x['id'])
        valid_article_ids = {str(art['id']) for art in sorted_articles}
        for art in sorted_articles:
            print("\nH E A D L I N E S")
            print(f"Article Id: {art['id']}")
            print(f"{art['title']}")
            if art.get("content"):
                print(f"{art['content'][:100]}...")
            print(f"source: {art['source']}")
            print(f"URL: {art['url']}")
            print(f"Category: {art['category']}")
            print("-" * 40)
        try:
            print("1. Back")
            print("2. Enter ID for more details")
            print("3. Logout")
            sub_choice = input("Enter your choice: ")
            if sub_choice == "1":
                break
            elif sub_choice == "2":
                article_id = input("Enter Article ID for more details: ")
                if not article_id.strip():
                    print("Error: Article ID cannot be empty.")
                    continue
                try:
                    int(article_id)
                except ValueError:
                    print("Error: Article ID must be a number.")
                    continue
                if article_id not in valid_article_ids:
                    print(f"Error: Article ID {article_id} is not in the current list. Please choose from the displayed articles.")
                    continue
                show_article_details_menu(article_id, user_id)
                print("\nRefreshing articles...")
                if view_type == "today":
                    today = datetime.now().strftime("%Y-%m-%d")
                    refresh_params = {"start": today, "end": today, "limit": 20}
                elif view_type == "date_range" and params:
                    refresh_params = params
                else:
                    refresh_params = {"limit": 20}
                try:
                    resp = requests.get(f"{API_URL}/news/headlines", params=refresh_params)
                    if resp.status_code == 200:
                        articles = resp.json()
                    else:
                        print("Failed to refresh articles. Using cached data.")
                except Exception as e:
                    print(f"Error refreshing articles: {e}. Using cached data.")
            elif sub_choice == "3":
                print("Logging out...")
                sys.exit(0)
            else:
                print("Invalid choice. Try again.")
        except KeyboardInterrupt:
            print("\n\nGoodbye! Application terminated gracefully.")
            sys.exit(0)
        except EOFError:
            print("\n\nGoodbye! Application terminated gracefully.")
            sys.exit(0)

def display_search_results_with_refresh(articles, search_query):
    if not articles:
        print("No articles found for your search.")
        return
    session = get_session()
    user_id = session.get("user_id")
    while True:
        sorted_articles = sorted(articles, key=lambda x: x['id'])
        valid_article_ids = {str(art['id']) for art in sorted_articles}
        print("\nS E A R C H")
        for art in sorted_articles:
            print(f"Article Id: {art['id']} {art['title']}")
            if art.get("content"):
                print(f"{art['content'][:100]}...")
            print(f"source: {art['source']}")
            print(f"URL: {art['url']}")
            print(f"Category: {art['category']}")
            print("-" * 40)
        try:
            print("1. Back")
            print("2. Enter ID for more details")
            print("3. Logout")
            choice = input("Enter your choice: ")
            if choice == "1":
                break
            elif choice == "2":
                article_id = input("Enter Article ID for more details: ")
                if not article_id.strip():
                    print("Error: Article ID cannot be empty.")
                    continue
                try:
                    int(article_id)
                except ValueError:
                    print("Error: Article ID must be a number.")
                    continue
                if article_id not in valid_article_ids:
                    print(f"Error: Article ID {article_id} is not in the current list. Please choose from the displayed articles.")
                    continue
                show_article_details_menu(article_id, user_id)
                print("\nRefreshing search results...")
                try:
                    resp = requests.get(f"{API_URL}/news/search", params={"q": search_query})
                    if resp.status_code == 200:
                        articles = resp.json()
                    else:
                        print("Failed to refresh search results. Using cached data.")
                except Exception as e:
                    print(f"Error refreshing search results: {e}. Using cached data.")
            elif choice == "3":
                print("Logging out...")
                sys.exit(0)
            else:
                print("Invalid choice. Try again.")
        except KeyboardInterrupt:
            print("\n\nGoodbye! Application terminated gracefully.")
            sys.exit(0)
        except EOFError:
            print("\n\nGoodbye! Application terminated gracefully.")
            sys.exit(0)

def display_articles(articles, user_id):
    if not articles:
        print("No headlines found for the selected criteria.")
        return
    sorted_articles = sorted(articles, key=lambda x: x['id'])
    valid_article_ids = {str(art['id']) for art in sorted_articles}
    for art in sorted_articles:
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
        try:
            print("1. Back")
            print("2. Enter ID for more details")
            print("3. Logout")
            sub_choice = input("Enter your choice: ")
            if sub_choice == "1":
                break
            elif sub_choice == "2":
                article_id = input("Enter Article ID for more details: ")
                if not article_id.strip():
                    print("Error: Article ID cannot be empty.")
                    continue
                try:
                    int(article_id)
                except ValueError:
                    print("Error: Article ID must be a number.")
                    continue
                if article_id not in valid_article_ids:
                    print(f"Error: Article ID {article_id} is not in the current list. Please choose from the displayed articles.")
                    continue
                show_article_details_menu(article_id, user_id)
            elif sub_choice == "3":
                print("Logging out...")
                sys.exit(0)
            else:
                print("Invalid choice. Try again.")
        except KeyboardInterrupt:
            print("\n\nGoodbye! Application terminated gracefully.")
            sys.exit(0)
        except EOFError:
            print("\n\nGoodbye! Application terminated gracefully.")
            sys.exit(0)

def get_article_by_id(article_id):
    try:
        resp = requests.get(f"{API_URL}/news/{article_id}")
        if resp.status_code == 200:
            return resp.json()
        else:
            return None
    except Exception as e:
        print(f"Error fetching article: {e}")
        return None

def show_article_details_menu(article_id, user_id):
    try:
        article = get_article_by_id(article_id)
        if not article:
            print("Error: Article not found or could not be retrieved.")
            return
        print("\n" + "="*60)
        print("ARTICLE DETAILS")
        print("="*60)
        print(f"Article ID: {article['id']}")
        print(f"Title: {article['title']}")
        print(f"Source: {article['source']}")
        print(f"Category: {article['category']}")
        print(f"URL: {article['url']}")
        if article.get('content'):
            print(f"\nContent:")
            print(f"{article['content']}")
        print("="*60)
        while True:
            try:
                print("\n1. Save Article")
                print("2. Like Article")
                print("3. Dislike Article")
                print("4. Report Article")
                print("5. Back")
                choice = input("Enter your choice: ")
                if choice == "1":
                    try:
                        resp = requests.post(
                            f"{API_URL}/user/saved-articles",
                            params={"user_id": user_id, "article_id": article_id},
                        )
                        if resp.status_code == 200:
                            print(resp.json().get("message", "Article saved."))
                        else:
                            try:
                                error_data = resp.json()
                                print(f"Error: {error_data.get('detail', 'Failed to save article.')}")
                            except:
                                print("Error: Failed to save article.")
                    except Exception as e:
                        print(f"Error: {e}")
                elif choice == "2":
                    try:
                        resp = requests.post(
                            f"{API_URL}/news/{article_id}/like",
                            params={"user_id": user_id}
                        )
                        if resp.status_code == 200:
                            print(resp.json().get("message", "Article liked."))
                        else:
                            print("Failed to like article.")
                    except Exception as e:
                        print(f"Error: {e}")
                elif choice == "3":
                    try:
                        resp = requests.post(
                            f"{API_URL}/news/{article_id}/dislike",
                            params={"user_id": user_id}
                        )
                        if resp.status_code == 200:
                            print(resp.json().get("message", "Article disliked."))
                        else:
                            print("Failed to dislike article.")
                    except Exception as e:
                        print(f"Error: {e}")
                elif choice == "4":
                    try:
                        reason = input("Reason for reporting: ")
                        if not reason.strip():
                            print("Error: Reason for reporting cannot be empty.")
                            continue
                        
                        resp = requests.post(
                            f"{API_URL}/user/report-article",
                            json={"article_id": int(article_id), "user_id": user_id, "reason": reason.strip()},
                        )
                        
                        if resp.status_code == 200:
                            result = resp.json()
                            print(result.get("message", "Thank you for your feedback. The admin will review this article."))
                        else:
                            try:
                                error_data = resp.json()
                                print(f"Failed to report article: {error_data.get('detail', 'Unknown error')}")
                            except:
                                print("Failed to report article: Unknown error")
                    except Exception as e:
                        print(f"Error: {e}")
                elif choice == "5":
                    break
                else:
                    print("Invalid choice. Try again.")
            except KeyboardInterrupt:
                print("\n\nGoodbye! Application terminated gracefully.")
                sys.exit(0)
            except EOFError:
                print("\n\nGoodbye! Application terminated gracefully.")
                sys.exit(0)
    except KeyboardInterrupt:
        print("\n\nGoodbye! Application terminated gracefully.")
        sys.exit(0)
    except EOFError:
        print("\n\nGoodbye! Application terminated gracefully.")
        sys.exit(0)

def show_saved_articles_menu():
    try:
        session = get_session()
        user_id = session.get("user_id")
        resp = requests.get(f"{API_URL}/user/saved-articles", params={"user_id": user_id})
        articles = resp.json()
        if not articles:
            print("No saved articles found.")
        else:
            sorted_articles = sorted(articles, key=lambda x: x['id'])
            print("\nS A V E D")
            for art in sorted_articles:
                print(f"Article Id: {art['id']} {art['title']}")
                if art.get("content"):
                    print(f"{art['content'][:100]}...")
                print(f"source: {art['source']}")
                print(f"URL: {art['url']}")
                print(f"Category: {art['category']}")
                print("-" * 40)
        while True:
            try:
                print("1. Delete Article")
                print("2. Report Article")
                print("3. Back")
                choice = input("Enter your choice: ")
                if choice == "1":
                    article_id = input("Enter Article ID to delete: ")
                    resp = requests.delete(
                        f"{API_URL}/user/saved-articles/{article_id}", params={"user_id": user_id}
                    )
                    print(resp.json().get("message", "Article id does not exist to be deleted."))
                elif choice == "2":
                    article_id = input("Enter Article ID to report: ")
                    if not article_id.strip():
                        print("Error: Article ID cannot be empty.")
                        continue
                    try:
                        int(article_id)
                    except ValueError:
                        print("Error: Article ID must be a number.")
                        continue
                    
                    reason = input("Reason for reporting: ")
                    if not reason.strip():
                        print("Error: Reason for reporting cannot be empty.")
                        continue
                    
                    resp = requests.post(
                        f"{API_URL}/user/report-article",
                        json={"article_id": int(article_id), "user_id": user_id, "reason": reason.strip()},
                    )
                    
                    if resp.status_code == 200:
                        result = resp.json()
                        print(result.get("message", "Thank you for your feedback. The admin will review this article."))
                    else:
                        try:
                            error_data = resp.json()
                            print(f"Failed to report article: {error_data.get('detail', 'Unknown error')}")
                        except:
                            print("Failed to report article: Unknown error")
                elif choice == "3":
                    break
                else:
                    print("Invalid choice. Try again.")
            except KeyboardInterrupt:
                print("\n\nGoodbye! Application terminated gracefully.")
                sys.exit(0)
            except EOFError:
                print("\n\nGoodbye! Application terminated gracefully.")
                sys.exit(0)
    except KeyboardInterrupt:
        print("\n\nGoodbye! Application terminated gracefully.")
        sys.exit(0)
    except EOFError:
        print("\n\nGoodbye! Application terminated gracefully.")
        sys.exit(0)

def search_articles():
    try:
        q = input("Enter search query: ")
        if not q or not q.strip():
            print("Error: Search query cannot be empty.")
            return
        search_query = q.strip()
        resp = requests.get(f"{API_URL}/news/search", params={"q": search_query})
        articles = resp.json()
        if not articles:
            print("No articles found for your search.")
        else:
            display_search_results_with_refresh(articles, search_query)
    except KeyboardInterrupt:
        print("\n\nGoodbye! Application terminated gracefully.")
        sys.exit(0)
    except EOFError:
        print("\n\nGoodbye! Application terminated gracefully.")
        sys.exit(0)

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
            resp = requests.get(f"{API_URL}/user/notification-articles", params={"user_id": user_id})
            articles = resp.json()
            if not articles:
                print("No notifications found for your settings.")
            else:
                print("\nYour News Notifications:")
                for art in articles:
                    print(f"\nArticle Id: {art['id']}")
                    print(f"Title: {art['title']}")
                    print(f"Source: {art['source']}")
                    print(f"Category: {art['category']}")
                    print(f"URL: {art['url']}")
                    print("-" * 40)
                while True:
                    print("1. Back")
                    print("2. Enter ID for more details")
                    print("3. Logout")
                    sub_choice = input("Enter your choice: ")
                    if sub_choice == "1":
                        break
                    elif sub_choice == "2":
                        article_id = input("Enter Article ID for more details: ")
                        show_article_details_menu(article_id, user_id)
                    elif sub_choice == "3":
                        print("Logging out...")
                        sys.exit(0)
                    else:
                        print("Invalid choice. Try again.")
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
    notif_dict = {n["type"].lower(): n for n in notifications}
    while True:
        print("\nC O N F I G U R E - N O T I F I C A T I O N S")
        for idx, cat in enumerate(categories, 1):
            enabled = notif_dict.get(cat["name"].lower(), {}).get("enabled", False)
            try:
                enabled = int(enabled) == 1
            except Exception:
                enabled = str(enabled).lower() == "true"
            keywords = notif_dict.get(cat["name"].lower(), {}).get("keywords", "")
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
            current = notif_dict.get(cat_name.lower(), {}).get("enabled", False)
            try:
                current = int(current) == 1
            except Exception:
                current = str(current).lower() == "true"
            keywords = notif_dict.get(cat_name.lower(), {}).get("keywords", "")
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
                        notif_dict[cat_name.lower()] = {
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
                        notif_dict[cat_name.lower()] = {
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
                        notif_dict[cat_name.lower()] = {
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
    try:
        session = get_session()
        user_id = session.get("user_id")
        
        article_id = input("Enter Article ID to report: ")
        
        # Validate article ID
        if not article_id.strip():
            print("Error: Article ID cannot be empty.")
            return
        
        try:
            int(article_id)
        except ValueError:
            print("Error: Article ID must be a number.")
            return
        
        reason = input("Reason for reporting: ")
        
        # Validate reason
        if not reason.strip():
            print("Error: Reason for reporting cannot be empty.")
            return
        
        resp = requests.post(
            f"{API_URL}/user/report-article",
            json={"article_id": int(article_id), "user_id": user_id, "reason": reason.strip()},
        )
        
        if resp.status_code == 200:
            result = resp.json()
            print(result.get("message", "Thank you for your feedback. The admin will review this article."))
        else:
            try:
                error_data = resp.json()
                print(f"Failed to report article: {error_data.get('detail', 'Unknown error')}")
            except:
                print("Failed to report article: Unknown error")
                
    except KeyboardInterrupt:
        print("\n\nGoodbye! Application terminated gracefully.")
        sys.exit(0)
    except EOFError:
        print("\n\nGoodbye! Application terminated gracefully.")
        sys.exit(0)
    except Exception as e:
        print(f"Error reporting article: {e}")
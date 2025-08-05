import sys
import requests

API_URL = "http://localhost:8000/admin"

def view_sources():
    try:
        resp = requests.get(f"{API_URL}/external-sources")
        if resp.status_code == 200:
            sources = resp.json()
            if not sources:
                print("No external sources found.")
            else:
                print("\nList of external servers:")
                for src in sources:
                    last_accessed = src['last_accessed'] if src['last_accessed'] else "Never"
                    print(f"{src['id']}. {src['name']} - {'Active' if src['status'] else 'Not Active'} - last accessed: {last_accessed}")
        else:
            print("Failed to fetch sources. Server returned:", resp.status_code)
    except Exception as e:
        print("Error fetching sources:", e)
    print()

def view_source_details():
    try:
        resp = requests.get(f"{API_URL}/external-sources")
        if resp.status_code == 200:
            sources = resp.json()
            if not sources:
                print("No external sources found.")
            else:
                print("\nList of external server details:\n")
                for idx, src in enumerate(sources, 1):
                    print(f"{idx}. {src['name']} - {src['api_key']}")
        else:
            print("Failed to fetch sources. Server returned:", resp.status_code)
    except Exception as e:
        print("Error fetching sources:", e)
    print()

def update_source():
    try:
        source_id = input("Enter external server ID: ")
        api_key = input("Enter the updated API key: ")
        
        # Client-side validation
        if not api_key or not api_key.strip():
            print("API key cannot be empty or blank.")
            return
        
        try:
            resp = requests.put(f"{API_URL}/external-sources/{source_id}", json={"api_key": api_key.strip()})
            if resp.status_code == 200:
                print(resp.json().get("message", "Source updated."))
            else:
                try:
                    error_data = resp.json()
                    if "detail" in error_data:
                        if isinstance(error_data["detail"], list):
                            for error in error_data["detail"]:
                                print(f"Validation error: {error.get('msg', 'Unknown error')}")
                        else:
                            print(f"Error: {error_data['detail']}")
                    else:
                        print("Failed to update source. Server returned:", resp.status_code)
                except:
                    print("Failed to update source. Server returned:", resp.status_code)
        except Exception as e:
            print("Error updating source:", e)
    except KeyboardInterrupt:
        print("\n\nGoodbye! Application terminated gracefully.")
        sys.exit(0)
    except EOFError:
        print("\n\nGoodbye! Application terminated gracefully.")
        sys.exit(0)

def add_category():
    try:
        name = input("Enter new category name: ")
        description = input("Enter category description: ")
        
        # Client-side validation
        if not name or not name.strip():
            print("Error: Category name cannot be empty or blank.")
            return
        
        try:
            resp = requests.post(f"{API_URL}/categories", json={"name": name.strip(), "description": description if description.strip() else None})
            if resp.status_code == 200:
                print(resp.json().get("message", "Category added."))
            else:
                try:
                    error_data = resp.json()
                    if "detail" in error_data:
                        if isinstance(error_data["detail"], list):
                            for error in error_data["detail"]:
                                print(f"Validation error: {error.get('msg', 'Unknown error')}")
                        else:
                            print(f"Error: {error_data['detail']}")
                    else:
                        print("Failed to add category. Server returned:", resp.status_code)
                except:
                    print("Failed to add category. Server returned:", resp.status_code)
        except Exception as e:
            print("Error adding category:", e)
    except KeyboardInterrupt:
        print("\n\nGoodbye! Application terminated gracefully.")
        sys.exit(0)
    except EOFError:
        print("\n\nGoodbye! Application terminated gracefully.")
        sys.exit(0)

def add_source():
    name = input("Enter new source name: ")
    api_key = input("Enter API key: ")
    
    # Client-side validation
    if not name or not name.strip():
        print("Error: Source name cannot be empty or blank.")
        return
    
    if not api_key or not api_key.strip():
        print("Error: API key cannot be empty or blank.")
        return
    
    try:
        resp = requests.post(f"{API_URL}/external-sources", json={"name": name.strip(), "api_key": api_key.strip()})
        if resp.status_code == 200:
            print(resp.json().get("message", "Source added."))
        else:
            try:
                error_data = resp.json()
                if "detail" in error_data:
                    if isinstance(error_data["detail"], list):
                        for error in error_data["detail"]:
                            print(f"Validation error: {error.get('msg', 'Unknown error')}")
                    else:
                        print(f"Error: {error_data['detail']}")
                else:
                    print("Failed to add source. Server returned:", resp.status_code)
            except:
                print("Failed to add source. Server returned:", resp.status_code)
    except Exception as e:
        print("Error adding source:", e)

def view_reported_articles():
    try:
        resp = requests.get(f"{API_URL}/reported-articles")
        articles = resp.json()
        if not articles or not isinstance(articles, list):
            print("No reported articles found.")
            return
        
        print("\n" + "="*60)
        print("REPORTED ARTICLES")
        print("="*60)
        
        for art in articles:
            if not isinstance(art, dict):
                print("Warning: Skipping invalid article:", art)
                continue
            
            print(f"\nArticle ID: {art['id']}")
            print(f"Title: {art['title']}")
            print(f"Source: {art['source']}")
            print(f"Category: {art['category']}")
            print(f"Total Reports: {art['report_count']}")
            print(f"Status: {'HIDDEN' if art.get('hidden', 0) else 'VISIBLE'}")
            
            # Show reasons if available
            if art.get('reasons'):
                print(f"Reasons: {art['reasons']}")
            
            print("-" * 60)
        
        # Provide options for detailed view and actions
        while True:
            try:
                print("\nOptions:")
                print("1. View detailed report for specific article")
                print("2. Hide/Unhide article")
                print("3. Back to main menu")
                choice = input("Enter your choice: ")
                
                if choice == "1":
                    article_id = input("Enter Article ID to view detailed reports: ")
                    if article_id.strip():
                        view_article_report_details(article_id.strip())
                elif choice == "2":
                    hide_unhide_article()
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
                
    except Exception as e:
        print(f"Error viewing reported articles: {e}")

def view_article_report_details(article_id):
    """View detailed report information for a specific article."""
    try:
        resp = requests.get(f"{API_URL}/reported-articles/{article_id}/details")
        if resp.status_code == 200:
            reports = resp.json()
            if not reports:
                print(f"No detailed reports found for article {article_id}")
                return
            
            print(f"\n" + "="*60)
            print(f"DETAILED REPORTS FOR ARTICLE {article_id}")
            print("="*60)
            
            for report in reports:
                print(f"\nReport ID: {report['id']}")
                print(f"Reason: {report['reason']}")
                print(f"Reported by: {report['username'] or f'User {report['user_id']}'}")
                print(f"Reported at: {report['reported_at']}")
                print("-" * 40)
        else:
            print(f"Failed to get report details. Server returned: {resp.status_code}")
    except Exception as e:
        print(f"Error viewing report details: {e}")

def view_hidden_articles():
    """View all hidden articles."""
    try:
        resp = requests.get(f"{API_URL}/hidden-articles")
        if resp.status_code == 200:
            articles = resp.json()
            if not articles:
                print("No hidden articles found.")
                return
            
            print("\n" + "="*60)
            print("HIDDEN ARTICLES")
            print("="*60)
            
            for art in articles:
                print(f"\nArticle ID: {art['id']}")
                print(f"Title: {art['title']}")
                print(f"Source: {art['source']}")
                print(f"Category: {art['category']}")
                print(f"Published: {art['published_at']}")
                print("-" * 60)
            
            # Provide option to unhide articles
            while True:
                try:
                    print("\nOptions:")
                    print("1. Unhide specific article")
                    print("2. Back to main menu")
                    choice = input("Enter your choice: ")
                    
                    if choice == "1":
                        article_id = input("Enter Article ID to unhide: ")
                        if article_id.strip():
                            try:
                                resp = requests.post(f"{API_URL}/articles/{article_id}/toggle-visibility", params={"hide": False})
                                if resp.status_code == 200:
                                    print(resp.json().get("message", "Article unhidden successfully."))
                                else:
                                    print("Failed to unhide article.")
                            except Exception as e:
                                print(f"Error unhiding article: {e}")
                    elif choice == "2":
                        break
                    else:
                        print("Invalid choice. Try again.")
                except KeyboardInterrupt:
                    print("\n\nGoodbye! Application terminated gracefully.")
                    sys.exit(0)
                except EOFError:
                    print("\n\nGoodbye! Application terminated gracefully.")
                    sys.exit(0)
        else:
            print(f"Failed to get hidden articles. Server returned: {resp.status_code}")
    except Exception as e:
        print(f"Error viewing hidden articles: {e}")

def hide_unhide_article():
    try:
        article_id = input("Enter Article ID to hide/unhide: ")
        if not article_id.strip():
            print("Error: Article ID cannot be empty.")
            return
        
        try:
            int(article_id)
        except ValueError:
            print("Error: Article ID must be a number.")
            return
        
        # First, get current article status
        resp = requests.get(f"{API_URL}/reported-articles")
        if resp.status_code == 200:
            articles = resp.json()
            article = next((art for art in articles if art.get('id') == int(article_id)), None)
            
            if not article:
                print(f"Error: Article {article_id} not found in reported articles.")
                return
            
            current_status = "HIDDEN" if article.get('hidden', 0) else "VISIBLE"
            print(f"Current status: {current_status}")
            
            # Ask for new status
            action = input(f"Make article {'VISIBLE' if current_status == 'HIDDEN' else 'HIDDEN'}? (yes/no): ").strip().lower()
            if action == "yes":
                new_hide_status = current_status == "VISIBLE"  # Hide if currently visible, show if currently hidden
                
                resp = requests.post(f"{API_URL}/articles/{article_id}/toggle-visibility", params={"hide": new_hide_status})
                if resp.status_code == 200:
                    print(resp.json().get("message", "Article status updated successfully."))
                else:
                    print("Failed to update article status.")
            else:
                print("Operation cancelled.")
        else:
            print("Failed to get article information.")
            
    except KeyboardInterrupt:
        print("\n\nGoodbye! Application terminated gracefully.")
        sys.exit(0)
    except EOFError:
        print("\n\nGoodbye! Application terminated gracefully.")
        sys.exit(0)
    except Exception as e:
        print(f"Error updating article status: {e}")

def hide_unhide_category():
    category = input("Enter category name to hide/unhide: ")
    hide = input("Hide this category? (yes/no): ").strip().lower() == "yes"
    resp = requests.post(f"{API_URL}/hide-category", params={"category": category, "hide": hide})
    print(resp.json().get("message", "Failed to update category."))

def manage_filtered_keywords():
    while True:
        try:
            print("\nManage Filtered Keywords:")
            print("1. View Keywords")
            print("2. Add Keyword")
            print("3. Remove Keyword")
            print("4. Back")
            choice = input("Enter your choice: ")
            if choice == "1":
                resp = requests.get(f"{API_URL}/filtered-keywords")
                keywords = resp.json()
                print("Filtered Keywords:", ", ".join(keywords) if keywords else "None")
            elif choice == "2":
                keyword = input("Enter keyword to add: ").strip()
                if not keyword:
                    print("Error: Keyword cannot be empty.")
                    continue
                resp = requests.post(f"{API_URL}/filtered-keywords", json={"keyword": keyword})
                if resp.status_code == 200:
                    print(resp.json().get("message", "Keyword added."))
                else:
                    try:
                        error_data = resp.json()
                        if "detail" in error_data:
                            if isinstance(error_data["detail"], list):
                                for error in error_data["detail"]:
                                    print(f"Validation error: {error.get('msg', 'Unknown error')}")
                            else:
                                print(f"Error: {error_data['detail']}")
                        else:
                            print("Failed to add keyword. Server returned:", resp.status_code)
                    except:
                        print("Failed to add keyword. Server returned:", resp.status_code)
            elif choice == "3":
                keyword = input("Enter keyword to remove: ").strip()
                if not keyword:
                    print("Error: Keyword cannot be empty.")
                    continue
                resp = requests.delete(f"{API_URL}/filtered-keywords", json={"keyword": keyword})
                if resp.status_code == 200:
                    print(resp.json().get("message", "Keyword removed."))
                else:
                    try:
                        error_data = resp.json()
                        if "detail" in error_data:
                            if isinstance(error_data["detail"], list):
                                for error in error_data["detail"]:
                                    print(f"Validation error: {error.get('msg', 'Unknown error')}")
                            else:
                                print(f"Error: {error_data['detail']}")
                        else:
                            print("Failed to remove keyword. Server returned:", resp.status_code)
                    except:
                        print("Failed to remove keyword. Server returned:", resp.status_code)
            elif choice == "4":
                break
            else:
                print("Invalid choice. Try again.")
        except KeyboardInterrupt:
            print("\n\nGoodbye! Application terminated gracefully.")
            sys.exit(0)
        except EOFError:
            print("\n\nGoodbye! Application terminated gracefully.")
            sys.exit(0)
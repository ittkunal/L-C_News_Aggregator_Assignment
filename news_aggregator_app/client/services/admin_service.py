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
    print()  # Adds a blank line after the list

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
    print()  # Adds a blank line after the list

def update_source():
    source_id = input("Enter external server ID: ")
    api_key = input("Enter the updated API key: ")
    try:
        resp = requests.put(f"{API_URL}/external-sources/{source_id}", params={"api_key": api_key})
        if resp.status_code == 200:
            print(resp.json().get("message", "Source updated."))
        else:
            print("Failed to update source. Server returned:", resp.status_code)
    except Exception as e:
        print("Error updating source:", e)

def add_category():
    name = input("Enter new category name: ")
    description = input("Enter category description: ")
    try:
        resp = requests.post(f"{API_URL}/categories", params={"name": name, "description": description})
        if resp.status_code == 200:
            print(resp.json().get("message", "Category added."))
        else:
            print("Failed to add category. Server returned:", resp.status_code)
    except Exception as e:
        print("Error adding category:", e)

def view_reported_articles():
    resp = requests.get(f"{API_URL}/reported-articles")
    articles = resp.json()
    if not articles or not isinstance(articles, list):
        print("No reported articles found.")
        return
    print("\nReported Articles:")
    for art in articles:
        if not isinstance(art, dict):
            print("Warning: Skipping invalid article:", art)
            continue
        print(f"Article Id: {art['id']}")
        print(f"Title: {art['title']}")
        print(f"Reports: {art['report_count']}")
        print(f"Hidden: {'Yes' if art.get('hidden', 0) else 'No'}")
        print("-" * 40)

def hide_unhide_article():
    article_id = input("Enter Article ID to hide/unhide: ")
    hide = input("Hide this article? (yes/no): ").strip().lower() == "yes"
    resp = requests.post(f"{API_URL}/hide-article", params={"article_id": article_id, "hide": hide})
    print(resp.json().get("message", "Failed to update article."))

def hide_unhide_category():
    category = input("Enter category name to hide/unhide: ")
    hide = input("Hide this category? (yes/no): ").strip().lower() == "yes"
    resp = requests.post(f"{API_URL}/hide-category", params={"category": category, "hide": hide})
    print(resp.json().get("message", "Failed to update category."))

def manage_filtered_keywords():
    while True:
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
            resp = requests.post(f"{API_URL}/filtered-keywords", params={"keyword": keyword})
            print(resp.json().get("message", "Failed to add keyword."))
        elif choice == "3":
            keyword = input("Enter keyword to remove: ").strip()
            resp = requests.delete(f"{API_URL}/filtered-keywords", params={"keyword": keyword})
            print(resp.json().get("message", "Failed to remove keyword."))
        elif choice == "4":
            break
        else:
            print("Invalid choice. Try again.")
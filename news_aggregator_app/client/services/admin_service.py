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

def view_source_details():
    source_id = input("Enter external server ID: ")
    try:
        resp = requests.get(f"{API_URL}/external-sources/{source_id}")
        if resp.status_code == 200:
            src = resp.json()
            print(f"\nName: {src['name']}\nAPI Key: {src['api_key']}\nStatus: {'Active' if src['status'] else 'Not Active'}")
        else:
            print("Source not found or server error.")
    except Exception as e:
        print("Error fetching source details:", e)

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
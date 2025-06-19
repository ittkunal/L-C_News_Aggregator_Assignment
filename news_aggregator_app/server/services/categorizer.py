CATEGORIES = {
    "business": ["business", "market", "stock", "finance", "economy"],
    "entertainment": ["entertainment", "movie", "music", "celebrity", "show"],
    "sports": ["sports", "game", "tournament", "player", "team"],
    "technology": ["technology", "tech", "software", "hardware", "gadget"],
}

def categorize_article(text: str) -> str:
    text = text.lower()
    for category, keywords in CATEGORIES.items():
        if any(word in text for word in keywords):
            return category
    return "general"
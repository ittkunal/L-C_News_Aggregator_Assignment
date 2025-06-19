from server.repositories.notification_repo import get_notifications_by_user
from server.repositories.user_repo import get_all_users
from server.repositories.article_repo import get_recent_articles
from server.services.mailer import send_email

def send_batch_notifications():
    users = get_all_users()
    for user in users:
        user_id = user["id"]
        email = user["email"]
        notifications = get_notifications_by_user(user_id)
        notif_dict = {n["type"]: n for n in notifications}
        matched_articles = []
        articles = get_recent_articles(hours=3)
        for article in articles:
            category = article["category"]
            notif = notif_dict.get(category)
            if notif and notif.get("enabled"):
                keywords = notif.get("keywords", "")
                if not keywords.strip():
                    continue 
                keyword_list = [k.strip().lower() for k in keywords.split(",") if k.strip()]
                text = (article.get("title", "") + " " + article.get("content", "")).lower()
                if any(kw in text for kw in keyword_list):
                    matched_articles.append(article)
        if matched_articles:
            body = "Here are your news notifications:\n\n"
            for art in matched_articles:
                body += f"- {art['title']} (Category: {art['category']})\n  {art.get('url', '')}\n\n"
            send_email(email, "Your News Digest", body)
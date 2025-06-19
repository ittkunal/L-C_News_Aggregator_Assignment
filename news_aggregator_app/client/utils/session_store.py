session = {}

def set_session(user_id, is_admin, username=None):
    session["user_id"] = user_id
    session["is_admin"] = is_admin
    if username:
        session["username"] = username

def get_session():
    return session
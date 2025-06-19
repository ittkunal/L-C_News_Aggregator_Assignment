from fastapi import HTTPException
from server.repositories.user_repo import get_user_by_email, create_user, get_user_by_username
from server.utils.validators import hash_password, verify_password

def login_user(user):
    db_user = get_user_by_username(user.username)
    if not db_user or not verify_password(user.password, db_user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {
        "message": "Login successful",
        "user_id": db_user["id"],
        "is_admin": db_user["is_admin"],
        "username": db_user["username"]
    }

def signup_user(user):
    if get_user_by_email(user.email):
        raise HTTPException(status_code=400, detail="User already exists")
    hashed_pw = hash_password(user.password)
    user_id = create_user(user.username, user.email, hashed_pw)
    return {"message": "Signup successful", "user_id": user_id}
import re
from email_validator import validate_email, EmailNotValidError

def validate_email_address(email: str) -> bool:
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False

def validate_username(username: str) -> bool:
    return bool(re.match(r"^[a-zA-Z0-9_]{3,30}$", username))

def validate_password(password: str) -> bool:
    return len(password) >= 6
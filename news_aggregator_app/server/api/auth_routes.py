from fastapi import APIRouter
from server.schemas.auth_schema import UserLogin, UserSignup
from server.controllers.auth_controller import login_user, signup_user

router = APIRouter()

@router.post("/login")
def login(user: UserLogin):
    return login_user(user)

@router.post("/signup")
def signup(user: UserSignup):
    return signup_user(user)
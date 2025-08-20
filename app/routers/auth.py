from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from bson import ObjectId
from app.schemas.token import Token
from app.services.auth import AuthService
from app.dependencies import get_current_user
from app.services.user import UserService
from app.services.client import ClientService

router = APIRouter()

@router.post("/register", response_model=Token)
def register(form_data: OAuth2PasswordRequestForm = Depends()):
    # Assuming register uses same form; in production, separate schema
    user_data = {"email": form_data.username, "password": form_data.password, "name": "", "phone": ""}
    user_id = UserService.create_user(user_data)  # Add name/phone via separate endpoint if needed
    user = UserService.collection.find_one({"_id": ObjectId(user_id)})
    return AuthService.create_token_for_user(user)
   
@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = AuthService.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return AuthService.create_token_for_user(user)

# @router.post("/logout")
# def logout(current_user: dict = Depends(get_current_user), token: str = Depends(oauth2_scheme)):
#     AuthService.logout(token)
#     return {"message": "Logged out"}

@router.post("/client/register", response_model=Token)
def register_client(form_data: OAuth2PasswordRequestForm = Depends()):
    # Assuming register uses same form; in production, separate schema
    client_data = {
        "name": form_data.username, 
        "password": form_data.password, 
        "phone": "", 
        "address": ""
    }
    client_id = ClientService.create_client(client_data)  # Add phone/address via separate endpoint if needed
    client = ClientService.collection.find_one({"_id": ObjectId(client_id)})
    return AuthService.create_token_for_client(client)

@router.post("/client/login", response_model=Token)
def login_client(form_data: OAuth2PasswordRequestForm = Depends()):
    client = AuthService.authenticate_client(form_data.username, form_data.password)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect client name or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return AuthService.create_token_for_client(client)
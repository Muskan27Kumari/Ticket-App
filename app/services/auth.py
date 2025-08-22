from passlib.context import CryptContext
from datetime import timedelta
from app.config import settings
from app.dependencies import create_access_token
from app.database import db
# from app.utils import blacklisted_tokens


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# blacklisted_tokens: set = set()

class AuthService:
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)

    @staticmethod
    def authenticate_user(email: str, password: str):
        user = db.users.find_one({"email": email})
        if not user or not AuthService.verify_password(password, user["password"]):
            return False
        return user

    # @staticmethod
    # def authenticate_client(name: str, password: str):
    #     client = db.clients.find_one({"name": name})
    #     if not client or not AuthService.verify_password(password, client["password"]):
    #         return False
    #     return client

    @staticmethod
    def create_token_for_user(user: dict):
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user["email"]}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    # @staticmethod
    # def create_token_for_client(client: dict):
    #     access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    #     access_token = create_access_token(
    #         data={"sub": client["name"]}, expires_delta=access_token_expires
    #     )
    #     return {"access_token": access_token, "token_type": "bearer"}

    # @staticmethod
    # def logout(token: str):
    #     blacklisted_tokens.add(token)
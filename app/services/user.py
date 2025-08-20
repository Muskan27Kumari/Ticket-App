from bson import ObjectId
from fastapi import HTTPException, status
from datetime import datetime
from app.database import db
from app.services.auth import AuthService
from app.models.user import UserModel

class UserService:
    collection = db.users

    @staticmethod
    def create_user(user_data: dict):
        if UserService.collection.find_one({"email": user_data["email"]}):
            raise HTTPException(status_code=400, detail="Email already registered")
        user_data["password"] = AuthService.get_password_hash(user_data["password"])
        user_model = UserModel(**user_data)
        result = UserService.collection.insert_one(user_model.dict(exclude={"id"}))
        return str(result.inserted_id)

    @staticmethod
    def get_users():
        users = list(UserService.collection.find())
        for user in users:
            user["id"] = str(user["_id"])
            del user["_id"]
            user["tickets"] = [str(t) for t in user.get("tickets", [])]
        return users

    @staticmethod
    def get_user(user_id: str):
        try:
            user = UserService.collection.find_one({"_id": ObjectId(user_id)})
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            user["id"] = str(user["_id"])
            del user["_id"]
            user["tickets"] = [str(t) for t in user.get("tickets", [])]
            return user
        except:
            raise HTTPException(status_code=400, detail="Invalid user ID")

    @staticmethod
    def update_user(user_id: str, update_data: dict):
        try:
            if "password" in update_data:
                update_data["password"] = AuthService.get_password_hash(update_data["password"])
            update_data["updated_at"] = datetime.utcnow()
            result = UserService.collection.update_one(
                {"_id": ObjectId(user_id)}, {"$set": update_data}
            )
            if result.matched_count == 0:
                raise HTTPException(status_code=404, detail="User not found")
            return UserService.get_user(user_id)
        except:
            raise HTTPException(status_code=400, detail="Invalid user ID")

    @staticmethod
    def delete_user(user_id: str):
        try:
            result = UserService.collection.delete_one({"_id": ObjectId(user_id)})
            if result.deleted_count == 0:
                raise HTTPException(status_code=404, detail="User not found")
        except:
            raise HTTPException(status_code=400, detail="Invalid user ID")
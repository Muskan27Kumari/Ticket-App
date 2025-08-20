from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.schemas.user import UserCreate, UserUpdate, UserOut
from app.services.user import UserService
from app.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=str)
def create_user(user: UserCreate, current_user: dict = Depends(get_current_user)):
    return UserService.create_user(user.dict())

@router.get("/", response_model=List[UserOut])
def get_users(current_user: dict = Depends(get_current_user)):
    return UserService.get_users()

@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: str, current_user: dict = Depends(get_current_user)):
    return UserService.get_user(user_id)

@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: str, user: UserUpdate, current_user: dict = Depends(get_current_user)):
    return UserService.update_user(user_id, user.dict(exclude_unset=True))

@router.delete("/{user_id}")
def delete_user(user_id: str, current_user: dict = Depends(get_current_user)):
    UserService.delete_user(user_id)
    return {"message": "User deleted"}
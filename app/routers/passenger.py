from fastapi import APIRouter, Depends
from app.schemas.passenger import PassengerCreate, PassengerUpdate, PassengerOut
from app.services.passenger import PassengerService
from app.dependencies import get_current_user

router = APIRouter(prefix="/passengers", tags=["passengers"])

@router.post("/", response_model=str)
def create_passenger(passenger: PassengerCreate, current_user: dict = Depends(get_current_user)):
    return PassengerService.create_passenger(passenger.dict(), current_user)

@router.get("/{passenger_id}", response_model=PassengerOut)
def get_passenger(passenger_id: str, current_user: dict = Depends(get_current_user)):
    return PassengerService.get_passenger(passenger_id, current_user)

@router.put("/{passenger_id}", response_model=PassengerOut)
def update_passenger(passenger_id: str, passenger: PassengerUpdate, current_user: dict = Depends(get_current_user)):
    return PassengerService.update_passenger(passenger_id, passenger.dict(exclude_unset=True), current_user)

@router.delete("/{passenger_id}")
def delete_passenger(passenger_id: str, current_user: dict = Depends(get_current_user)):
    PassengerService.delete_passenger(passenger_id, current_user)
    return {"message": "Passenger deleted"}
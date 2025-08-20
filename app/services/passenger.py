from bson import ObjectId
from fastapi import HTTPException, status
from datetime import datetime
from app.database import db
from app.models.passenger import PassengerModel
from app.services.ticket import TicketService

class PassengerService:
    collection = db.passengers
    ticket_collection = db.tickets

    @staticmethod
    def create_passenger(passenger_data: dict, current_user: dict):
        if "ticket_id" not in passenger_data:
            raise HTTPException(status_code=400, detail="ticket_id required")
        # Check if ticket belongs to user
        TicketService.get_ticket(passenger_data["ticket_id"], current_user)
        passenger_model = PassengerModel(**passenger_data)
        result = PassengerService.collection.insert_one(passenger_model.dict(exclude={"id"}))
        # Add to ticket's passengers
        PassengerService.ticket_collection.update_one(
            {"_id": ObjectId(passenger_data["ticket_id"])}, {"$push": {"passengers": result.inserted_id}}
        )
        return str(result.inserted_id)

    @staticmethod
    def get_passenger(passenger_id: str, current_user: dict):
        try:
            passenger = PassengerService.collection.find_one({"_id": ObjectId(passenger_id)})
            if not passenger:
                raise HTTPException(status_code=404, detail="Passenger not found")
            # Check auth via ticket
            ticket = PassengerService.ticket_collection.find_one({"_id": passenger["ticket_id"]})
            user = db.users.find_one({"tickets": ticket["_id"]})
            if user["email"] != current_user["email"]:
                raise HTTPException(status_code=403, detail="Not authorized")
            passenger["id"] = str(passenger["_id"])
            del passenger["_id"]
            return passenger
        except:
            raise HTTPException(status_code=400, detail="Invalid passenger ID")

    # Similar for update_passenger, delete_passenger (mirror ticket, pull from array on delete)
    # Omitted for brevity
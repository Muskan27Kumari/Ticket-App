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
        
        # Prepare passenger data for database insertion
        db_passenger_data = {
            "name": passenger_data["name"],
            "aadhaar_card": passenger_data["aadhaar_card"],
            "age": passenger_data["age"],
            "gender": passenger_data["gender"],
            "phone_no": passenger_data["phone_no"],
            "ticket_id": ObjectId(passenger_data["ticket_id"]),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = PassengerService.collection.insert_one(db_passenger_data)
        
        # Add to ticket's passengers
        PassengerService.ticket_collection.update_one(
            {"_id": ObjectId(passenger_data["ticket_id"])}, 
            {"$push": {"passengers": result.inserted_id}}
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
            if not ticket:
                raise HTTPException(status_code=404, detail="Associated ticket not found")
            
            user = db.users.find_one({"tickets": ticket["_id"]})
            if not user or user["email"] != current_user["email"]:
                raise HTTPException(status_code=403, detail="Not authorized")
            
            # Convert ObjectId fields to strings for response
            passenger["id"] = str(passenger["_id"])
            del passenger["_id"]
            passenger["ticket_id"] = str(passenger["ticket_id"])
            return passenger
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid passenger ID: {str(e)}")

    @staticmethod
    def update_passenger(passenger_id: str, update_data: dict, current_user: dict):
        passenger = PassengerService.get_passenger(passenger_id, current_user)  # Check auth
        try:
            update_data["updated_at"] = datetime.utcnow()
            result = PassengerService.collection.update_one(
                {"_id": ObjectId(passenger_id)}, {"$set": update_data}
            )
            if result.matched_count == 0:
                raise HTTPException(status_code=404, detail="Passenger not found")
            return PassengerService.get_passenger(passenger_id, current_user)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid passenger ID: {str(e)}")

    @staticmethod
    def delete_passenger(passenger_id: str, current_user: dict):
        passenger = PassengerService.get_passenger(passenger_id, current_user)  # Check auth
        try:
            # Remove from ticket's passengers
            PassengerService.ticket_collection.update_one(
                {"_id": ObjectId(passenger["ticket_id"])}, 
                {"$pull": {"passengers": ObjectId(passenger_id)}}
            )
            PassengerService.collection.delete_one({"_id": ObjectId(passenger_id)})
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid passenger ID: {str(e)}")
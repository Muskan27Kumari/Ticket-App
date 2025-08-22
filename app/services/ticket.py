from bson import ObjectId
from fastapi import HTTPException, status
from datetime import datetime
from app.database import db
from app.models.ticket import TicketModel

class TicketService:
    collection = db.tickets
    user_collection = db.users

    @staticmethod
    def create_ticket(ticket_data: dict, current_user: dict):
        # Get user from database
        user = TicketService.user_collection.find_one({"email": current_user["email"]})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Prepare ticket data for database insertion
        db_ticket_data = {
            "from_location": ticket_data["from_location"],
            "to_location": ticket_data["to_location"],
            "price": ticket_data["price"],
            "date_of_journey": ticket_data["date_of_journey"],
            "user_id": user["_id"],  # Use ObjectId from database
            "passengers": [],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        # Insert into database
        result = TicketService.collection.insert_one(db_ticket_data)
        
        # Add to user's tickets
        TicketService.user_collection.update_one(
            {"_id": user["_id"]}, {"$push": {"tickets": result.inserted_id}}
        )
        
        return str(result.inserted_id)

    @staticmethod
    def get_ticket(ticket_id: str, current_user: dict):
        try:
            ticket = TicketService.collection.find_one({"_id": ObjectId(ticket_id)})
            if not ticket:
                raise HTTPException(status_code=404, detail="Ticket not found")
            user = TicketService.user_collection.find_one({"email": current_user["email"]})
            if ticket["user_id"] != user["_id"]:
                raise HTTPException(status_code=403, detail="Not authorized")
            
            # Convert ObjectId fields to strings for response
            ticket["id"] = str(ticket["_id"])
            del ticket["_id"]
            ticket["user_id"] = str(ticket["user_id"])
            ticket["passengers"] = [str(p) for p in ticket.get("passengers", [])]
            return ticket
        except:
            raise HTTPException(status_code=400, detail="Invalid ticket ID")

    @staticmethod
    def update_ticket(ticket_id: str, update_data: dict, current_user: dict):
        ticket = TicketService.get_ticket(ticket_id, current_user)  # Check auth
        try:
            update_data["updated_at"] = datetime.utcnow()
            result = TicketService.collection.update_one(
                {"_id": ObjectId(ticket_id)}, {"$set": update_data}
            )
            if result.matched_count == 0:
                raise HTTPException(status_code=404, detail="Ticket not found")
            return TicketService.get_ticket(ticket_id, current_user)
        except:
            raise HTTPException(status_code=400, detail="Invalid ticket ID")

    @staticmethod
    def delete_ticket(ticket_id: str, current_user: dict):
        ticket = TicketService.get_ticket(ticket_id, current_user)  # Check auth
        try:
            # Remove from user's tickets
            TicketService.user_collection.update_one(
                {"tickets": ObjectId(ticket_id)}, {"$pull": {"tickets": ObjectId(ticket_id)}}
            )
            TicketService.collection.delete_one({"_id": ObjectId(ticket_id)})
        except:
            raise HTTPException(status_code=400, detail="Invalid ticket ID")
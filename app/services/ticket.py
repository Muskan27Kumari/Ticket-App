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
        ticket_data["user_id"] = ObjectId(ticket_data["user_id"]) if "user_id" in ticket_data else None
        if not ticket_data.get("user_id"):
            user = TicketService.user_collection.find_one({"email": current_user["email"]})
            ticket_data["user_id"] = user["_id"]
        ticket_model = TicketModel(**ticket_data)
        result = TicketService.collection.insert_one(ticket_model.dict(exclude={"id"}))
        # Add to user's tickets
        TicketService.user_collection.update_one(
            {"_id": ticket_data["user_id"]}, {"$push": {"tickets": result.inserted_id}}
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
            ticket["id"] = str(ticket["_id"])
            del ticket["_id"]
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
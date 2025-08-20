from fastapi import APIRouter, Depends
from app.schemas.ticket import TicketCreate, TicketUpdate, TicketOut
from app.services.ticket import TicketService
from app.dependencies import get_current_user

router = APIRouter(prefix="/tickets", tags=["tickets"])

@router.post("/", response_model=str)
def create_ticket(ticket: TicketCreate, current_user: dict = Depends(get_current_user)):
    return TicketService.create_ticket(ticket.dict(), current_user)

@router.get("/{ticket_id}", response_model=TicketOut)
def get_ticket(ticket_id: str, current_user: dict = Depends(get_current_user)):
    return TicketService.get_ticket(ticket_id, current_user)

@router.put("/{ticket_id}", response_model=TicketOut)
def update_ticket(ticket_id: str, ticket: TicketUpdate, current_user: dict = Depends(get_current_user)):
    return TicketService.update_ticket(ticket_id, ticket.dict(exclude_unset=True), current_user)

@router.delete("/{ticket_id}")
def delete_ticket(ticket_id: str, current_user: dict = Depends(get_current_user)):
    TicketService.delete_ticket(ticket_id, current_user)
    return {"message": "Ticket deleted"}
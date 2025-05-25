from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Controllers.ticket_controller import TicketController
from Database.Adapters.ticket_adapter import TicketAdapter
from Database.database import get_db

router = APIRouter(prefix="/tickets", tags=["Tickets"])

def get_ticket_controller(db: Session = Depends(get_db)) -> TicketController:
    adapter = TicketAdapter(db)
    return TicketController(adapter)

@router.get("/")
def read_tickets(controller: TicketController = Depends(get_ticket_controller)):
    return controller.fetch_tickets()

@router.get("/{ticket_id}")
def read_ticket(ticket_id: int, controller: TicketController = Depends(get_ticket_controller)):
    ticket = controller.fetch_ticket(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket
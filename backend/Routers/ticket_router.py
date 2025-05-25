from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Controllers.ticket_controller import fetch_tickets, fetch_ticket
from Database.database import get_db

router = APIRouter(prefix="/tickets", tags=["Tickets"])

@router.get("/")
def read_tickets(db: Session = Depends(get_db)):
    return fetch_tickets(db)

@router.get("/{ticket_id}")
def read_ticket(ticket_id: int, db: Session = Depends(get_db)):
    try:
        return fetch_ticket(db, ticket_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Ticket not found")

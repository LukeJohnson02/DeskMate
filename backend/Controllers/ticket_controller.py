from sqlalchemy.orm import Session
from Database.Adapters.ticket_adapter import get_all_tickets, get_ticket_by_id


def fetch_tickets(db: Session):
    return get_all_tickets(db)

def fetch_ticket(db: Session, ticket_id: int):
    ticket = get_ticket_by_id(db, ticket_id)
    if not ticket:
        raise ValueError("Ticket not found")
    return ticket
from sqlalchemy.orm import Session
from Models import Ticket


def get_all_tickets(db: Session):
    return db.query(Ticket).all()

def get_ticket_by_id(db: Session, ticket_id: int):
    return db.query(Ticket).filter(Ticket.id == ticket_id).first()

def create_ticket(db: Session, ticket: Ticket):
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket
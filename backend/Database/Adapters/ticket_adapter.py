from sqlalchemy.orm import Session
from Models import Ticket


class TicketAdapter:
    def __init__(self, db: Session):
        self.db = db

    def get_ticket_by_id(self, ticket_id: int):
        return self.db.query(Ticket).filter(Ticket.id == ticket_id).first()

    def get_tickets_by_user(self, user_id: int):
        return self.db.query(Ticket).filter(Ticket.user_id == user_id).all()

    def get_all_tickets(self):
        return self.db.query(Ticket).all()

    def create_ticket(self, ticket: Ticket):
        self.db.add(ticket)
        self.db.commit()
        self.db.refresh(ticket)
        return ticket

    def update_ticket(self, ticket: Ticket):
        self.db.commit()
        self.db.refresh(ticket)
        return ticket

    def delete_ticket(self, ticket: Ticket):
        self.db.delete(ticket)
        self.db.commit()

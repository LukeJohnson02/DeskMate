from sqlalchemy.orm import Session
from Database.Adapters.ticket_adapter import TicketAdapter


class TicketController:
    def __init__(self, adapter: TicketAdapter):
        self.adapter = adapter

    def fetch_tickets(self):
        return self.adapter.get_all_tickets()

    def fetch_ticket(self, ticket_id: int):
        ticket = self.adapter.get_ticket_by_id(ticket_id)
        if not ticket:
            raise ValueError("Ticket not found")
        return ticket
from Database.Adapters.ticket_adapter import TicketAdapter
from Models import UserRole, Ticket
from Models.ticket_model import TicketStatus


class TicketController:
    def __init__(self, adapter: TicketAdapter):
        self.adapter = adapter

    def fetch_tickets(self, current_user):
        if current_user.role == UserRole.ADMIN:
            return self.adapter.get_all_tickets()
        else:
            return self.adapter.get_tickets_by_user(current_user.id)

    def fetch_ticket(self, ticket_id: int, current_user):
        ticket = self.adapter.get_ticket_by_id(ticket_id)
        if not ticket:
            raise ValueError("Ticket not found")
        if current_user.role != UserRole.ADMIN and ticket.user_id != current_user.id:
            raise PermissionError("Not authorised to view this ticket")
        return ticket

    def create_ticket(
        self, title: str, description: str, category_id: int, current_user
    ):
        new_ticket = Ticket(
            title=title,
            description=description,
            status=TicketStatus.OPEN,
            user_id=current_user.id,
            category_id=category_id,
        )
        return self.adapter.create_ticket(new_ticket)

    def update_ticket(
        self,
        ticket_id: int,
        title: str,
        description: str,
        status: TicketStatus,
        current_user,
    ):
        ticket = self.adapter.get_ticket_by_id(ticket_id)
        if not ticket:
            raise ValueError("Ticket not found")
        if current_user.role != UserRole.ADMIN and ticket.user_id != current_user.id:
            raise PermissionError("Not authorised to update this ticket")

        ticket.title = title
        ticket.description = description
        ticket.status = status
        return self.adapter.update_ticket(ticket)

    def delete_ticket(self, ticket_id: int, current_user):
        ticket = self.adapter.get_ticket_by_id(ticket_id)
        if not ticket:
            raise ValueError("Ticket not found")
        if current_user.role != UserRole.ADMIN and ticket.user_id != current_user.id:
            raise PermissionError("Not authorised to delete this ticket")

        self.adapter.delete_ticket(ticket)

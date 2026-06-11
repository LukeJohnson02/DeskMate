from Database.Adapters.ticket_adapter import TicketAdapter
from Models import UserRole, Ticket
from Models.ticket_model import TicketStatus


class TicketController:
    """
    Controller for managing support tickets. Handles creation, retrieval,
    updating, and deletion of tickets based on user roles and permissions.
    """

    def __init__(self, adapter: TicketAdapter):
        """
        Initialise the TicketController with a TicketAdapter.

        :param adapter: An instance of TicketAdapter to handle data operations.
        """
        self.adapter = adapter

    def fetch_tickets(self, current_user):
        """
        Fetch tickets available to the current user. Admins receive all tickets;
        regular users only see their own.

        :param current_user: The user requesting tickets.
        :return: A list of tickets relevant to the user.
        """
        if current_user.role == UserRole.ADMIN:
            return self.adapter.get_all_tickets()
        else:
            return self.adapter.get_tickets_by_user(current_user.id)

    def fetch_ticket(self, ticket_id: int, current_user):
        """
        Retrieve a specific ticket by ID, validating access permissions.

        :param ticket_id: ID of the ticket to retrieve.
        :param current_user: The user requesting the ticket.
        :return: The requested ticket.
        :raises ValueError: If the ticket is not found.
        :raises PermissionError: If the user is not authorised to view the ticket.
        """
        ticket = self.adapter.get_ticket_by_id(ticket_id)
        if not ticket:
            raise ValueError("Ticket not found")
        if current_user.role != UserRole.ADMIN and ticket.user_id != current_user.id:
            raise PermissionError("Not authorised to view this ticket")
        return ticket

    def create_ticket(
        self, title: str, description: str, category_id: int, current_user
    ):
        """
        Create a new support ticket.

        :param title: Title of the ticket.
        :param description: Description of the issue.
        :param category_id: ID of the category the ticket belongs to.
        :param current_user: The user creating the ticket.
        :return: The newly created ticket.
        """
        if not self.adapter.category_exists(category_id):
            raise ValueError("Category not found")

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
        category_id: int,
        current_user,
    ):
        """
        Update the details of an existing ticket. Restricted to admins and ticket owners.

        :param ticket_id: ID of the ticket to update.
        :param title: New title of the ticket.
        :param description: Updated description.
        :param status: Updated ticket status.
        :param category_id: Updated category ID.
        :param current_user: The user requesting the update.
        :return: The updated ticket.
        :raises ValueError: If the ticket does not exist.
        :raises PermissionError: If the user is not authorised to update the ticket.
        """
        ticket = self.adapter.get_ticket_by_id(ticket_id)
        if not ticket:
            raise ValueError("Ticket not found")
        if not self.adapter.category_exists(category_id):
            raise ValueError("Category not found")
        if current_user.role != UserRole.ADMIN and ticket.user_id != current_user.id:
            raise PermissionError("Not authorised to update this ticket")

        ticket.title = title
        ticket.description = description
        ticket.status = status
        ticket.category_id = category_id
        return self.adapter.update_ticket(ticket)

    def delete_ticket(self, ticket_id: int, current_user):
        """
        Delete an existing ticket. Restricted to admins and ticket owners.

        :param ticket_id: ID of the ticket to delete.
        :param current_user: The user requesting deletion.
        :raises ValueError: If the ticket is not found.
        :raises PermissionError: If the user is not authorised to delete the ticket.
        """
        ticket = self.adapter.get_ticket_by_id(ticket_id)
        if not ticket:
            raise ValueError("Ticket not found")
        if current_user.role != UserRole.ADMIN and ticket.user_id != current_user.id:
            raise PermissionError("Not authorised to delete this ticket")

        self.adapter.delete_ticket(ticket)

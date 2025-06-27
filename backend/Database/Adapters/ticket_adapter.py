from sqlalchemy.orm import Session
from Models import Ticket


class TicketAdapter:
    """
    Adapter for database operations related to tickets.
    """

    def __init__(self, db: Session):
        """
        Initialise the TicketAdapter with a database session.

        :param db: SQLAlchemy Session instance for database interaction.
        """
        self.db = db

    def get_ticket_by_id(self, ticket_id: int):
        """
        Retrieve a ticket by its ID.

        :param ticket_id: The ID of the ticket to fetch.
        :return: The Ticket object if found, else None.
        """
        return self.db.query(Ticket).filter(Ticket.id == ticket_id).first()

    def get_tickets_by_user(self, user_id: int):
        """
        Retrieve all tickets associated with a specific user.

        :param user_id: The ID of the user.
        :return: A list of Ticket objects belonging to the user.
        """
        return self.db.query(Ticket).filter(Ticket.user_id == user_id).all()

    def get_all_tickets(self):
        """
        Retrieve all tickets in the database.

        :return: A list of all Ticket objects.
        """
        return self.db.query(Ticket).all()

    def create_ticket(self, ticket: Ticket):
        """
        Add a new ticket to the database.

        :param ticket: The Ticket object to add.
        :return: The newly created Ticket object.
        """
        self.db.add(ticket)
        self.db.commit()
        self.db.refresh(ticket)
        return ticket

    def update_ticket(self, ticket: Ticket):
        """
        Commit updates to an existing ticket.

        :param ticket: The Ticket object to update.
        :return: The updated Ticket object.
        """
        self.db.commit()
        self.db.refresh(ticket)
        return ticket

    def delete_ticket(self, ticket: Ticket):
        """
        Remove a ticket from the database.

        :param ticket: The Ticket object to delete.
        """
        self.db.delete(ticket)
        self.db.commit()

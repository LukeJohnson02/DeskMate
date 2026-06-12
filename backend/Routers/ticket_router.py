"""FastAPI routes for support-ticket CRUD operations."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Authentication.Dependancies.auth import get_current_user
from Controllers.ticket_controller import TicketController
from Database.Adapters.ticket_adapter import TicketAdapter
from Database.database import get_db
from Models import User
from Models.ticket_model import TicketCreate, TicketRead, TicketUpdate

router = APIRouter(prefix="/tickets", tags=["Tickets"])


def get_ticket_controller(db: Session = Depends(get_db)) -> TicketController:
    """Build the ticket controller with a request-scoped database session."""

    adapter = TicketAdapter(db)
    return TicketController(adapter)


@router.get("/", response_model=list[TicketRead])
def read_tickets(
    current_user: User = Depends(get_current_user),
    controller: TicketController = Depends(get_ticket_controller),
):
    """Return tickets visible to the authenticated user."""

    return controller.fetch_tickets(current_user)


@router.get("/{ticket_id}", response_model=TicketRead)
def read_ticket(
    ticket_id: int,
    current_user: User = Depends(get_current_user),
    controller: TicketController = Depends(get_ticket_controller),
):
    """Return a single ticket after applying ownership and role checks."""

    try:
        return controller.fetch_ticket(ticket_id, current_user)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except PermissionError:
        raise HTTPException(status_code=403, detail="Not authorised")


@router.post("/", response_model=TicketRead)
def create_ticket(
    ticket_data: TicketCreate,
    current_user: User = Depends(get_current_user),
    controller: TicketController = Depends(get_ticket_controller),
):
    """Create a ticket for the authenticated user."""

    try:
        return controller.create_ticket(
            ticket_data.title,
            ticket_data.description,
            ticket_data.category_id,
            current_user,
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.put("/{ticket_id}", response_model=TicketRead)
def update_ticket(
    ticket_id: int,
    ticket_data: TicketUpdate,
    current_user: User = Depends(get_current_user),
    controller: TicketController = Depends(get_ticket_controller),
):
    """Update a ticket after validating ownership and category membership."""

    try:
        return controller.update_ticket(
            ticket_id,
            ticket_data.title,
            ticket_data.description,
            ticket_data.status,
            ticket_data.category_id,
            current_user,
        )
    except ValueError:
        raise HTTPException(status_code=404, detail="Ticket not found")
    except PermissionError:
        raise HTTPException(status_code=403, detail="Not authorised")


@router.delete("/{ticket_id}")
def delete_ticket(
    ticket_id: int,
    current_user: User = Depends(get_current_user),
    controller: TicketController = Depends(get_ticket_controller),
):
    """Delete a ticket when the authenticated user is allowed to do so."""

    try:
        controller.delete_ticket(ticket_id, current_user)
        return {"detail": "Ticket deleted successfully"}
    except ValueError:
        raise HTTPException(status_code=404, detail="Ticket not found")
    except PermissionError:
        raise HTTPException(status_code=403, detail="Not authorised")

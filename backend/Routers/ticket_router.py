from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Authentication.Dependancies.auth import get_current_user
from Controllers.ticket_controller import TicketController
from Database.Adapters.ticket_adapter import TicketAdapter
from Database.database import get_db
from Models import User
from Models.ticket_model import TicketStatus

router = APIRouter(prefix="/tickets", tags=["Tickets"])


def get_ticket_controller(db: Session = Depends(get_db)) -> TicketController:
    adapter = TicketAdapter(db)
    return TicketController(adapter)


@router.get("/")
def read_tickets(
    current_user: User = Depends(get_current_user),
    controller: TicketController = Depends(get_ticket_controller),
):
    return controller.fetch_tickets(current_user)


@router.get("/{ticket_id}")
def read_ticket(
    ticket_id: int,
    current_user: User = Depends(get_current_user),
    controller: TicketController = Depends(get_ticket_controller),
):
    try:
        return controller.fetch_ticket(ticket_id, current_user)
    except ValueError:
        raise HTTPException(status_code=404, detail="Ticket not found")
    except PermissionError:
        raise HTTPException(status_code=403, detail="Not authorised")


@router.post("/")
def create_ticket(
    title: str,
    description: str,
    category_id: int,
    current_user: User = Depends(get_current_user),
    controller: TicketController = Depends(get_ticket_controller),
):
    return controller.create_ticket(title, description, category_id, current_user)


@router.put("/{ticket_id}")
def update_ticket(
    ticket_id: int,
    title: str,
    description: str,
    status: TicketStatus,
    current_user: User = Depends(get_current_user),
    controller: TicketController = Depends(get_ticket_controller),
):
    try:
        return controller.update_ticket(
            ticket_id, title, description, status, current_user
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
    try:
        controller.delete_ticket(ticket_id, current_user)
        return {"detail": "Ticket deleted successfully"}
    except ValueError:
        raise HTTPException(status_code=404, detail="Ticket not found")
    except PermissionError:
        raise HTTPException(status_code=403, detail="Not authorised")

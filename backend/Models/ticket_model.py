"""Ticket database model and Pydantic request/response schemas."""

from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from enum import Enum
from Database.database import Base
from Models.common_model import CommonModel


class TicketStatus(str, Enum):
    """Allowed lifecycle states for a support ticket."""

    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    CLOSED = "CLOSED"


class TicketBase(BaseModel):
    """Fields shared by ticket create, update, and read schemas."""

    title: str = Field(..., min_length=3, max_length=120)
    description: str = Field(..., min_length=10, max_length=2000)
    category_id: int = Field(..., gt=0)


class TicketCreate(TicketBase):
    """Request body used when a user creates a ticket."""


class TicketUpdate(TicketBase):
    """Request body used when a ticket is edited."""

    status: TicketStatus


class TicketRead(TicketBase):
    """Response body returned by ticket endpoints."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    category_id: int
    status: TicketStatus
    user_id: int


class Ticket(CommonModel, Base):
    """SQLAlchemy ticket table linked to users and categories."""

    __tablename__ = "tickets"
    title = Column(String, index=True)
    description = Column(String)
    status = Column(SQLEnum(TicketStatus), default=TicketStatus.OPEN, nullable=False)

    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))

    # Relationships
    user = relationship("User", back_populates="tickets")
    category = relationship("Category", back_populates="tickets")

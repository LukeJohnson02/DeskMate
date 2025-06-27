from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from enum import Enum
from Database.database import Base
from Models.common_model import CommonModel


class TicketStatus(str, Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    CLOSED = "CLOSED"


class Ticket(CommonModel, Base):
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

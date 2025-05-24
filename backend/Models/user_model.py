from dataclasses import dataclass
from enum import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer
from typing import List
from Database.database import Base
from Models.ticket_model import Ticket


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"

@dataclass
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    role: Mapped[str] = mapped_column(String, default=UserRole.USER.value)

    tickets: Mapped[List["Ticket"]] = relationship("Ticket", back_populates="user")
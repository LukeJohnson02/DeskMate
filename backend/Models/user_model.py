"""User database model and authentication-related Pydantic schemas."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Column, Boolean, DateTime
from typing import List
from Database.database import Base
from Models.common_model import CommonModel
from Models.ticket_model import Ticket
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRole(str, Enum):
    """Supported application roles used for access control."""

    ADMIN = "admin"
    USER = "user"


@dataclass
class User(CommonModel, Base):
    """SQLAlchemy user table with credentials, role, and reset-token metadata."""

    __tablename__ = "users"
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, default=UserRole.USER.value)
    tickets: Mapped[List["Ticket"]] = relationship("Ticket", back_populates="user")
    is_verified = Column(Boolean, default=False, nullable=False)
    reset_token: str = Column(String, nullable=True)
    reset_token_expiry: datetime = Column(DateTime, nullable=True)


class UserRegister(BaseModel):
    """Request body used by the registration endpoint."""

    email: EmailStr
    name: str = Field(..., min_length=2, max_length=80)
    password: str = Field(..., min_length=8, max_length=128)


class UserLogin(BaseModel):
    """Credentials shape used by legacy login validation."""

    email: EmailStr
    password: str


class UserRead(BaseModel):
    """Public user response that excludes password and reset-token fields."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    role: UserRole
    is_verified: bool

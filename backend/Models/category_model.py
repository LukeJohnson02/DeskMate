from dataclasses import dataclass
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String
from typing import List
from Database.database import Base
from Models.common_model import CommonModel
from Models.ticket_model import Ticket
from pydantic import BaseModel, ConfigDict


class CategoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


@dataclass
class Category(CommonModel, Base):
    __tablename__ = "categories"
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    tickets: Mapped[List["Ticket"]] = relationship("Ticket", back_populates="category")

from dataclasses import dataclass
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String
from typing import List
from Database.database import Base
from Models.ticket import Ticket


@dataclass
class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    tickets: Mapped[List["Ticket"]] = relationship("Ticket", back_populates="category")
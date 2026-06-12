"""Shared SQLAlchemy fields used by all persisted models."""

from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class CommonModel:
    """Mixin that gives database tables a primary key and audit timestamps."""

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

from __future__ import annotations
from typing import List, Optional

from sqlalchemy import ForeignKey, String, DateTime, func
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)
from app.behaviour_db import Base


class Site(Base):
    __tablename__ = 'site'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    actions: Mapped[List["Action"]] = relationship()


class Action(Base):
    __tablename__ = "action"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    site_id: Mapped[int] = mapped_column(ForeignKey("site.id"))
    logs: Mapped[List["Log"]] = relationship()


class Log(Base):
    __tablename__ = "log"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    action_id: Mapped[int] = mapped_column(ForeignKey("action.id"))
    detail: Mapped[str] = mapped_column(String)
    email: Mapped[Optional[str]] = mapped_column(String)
    create_date: Mapped[Optional[DateTime]] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )

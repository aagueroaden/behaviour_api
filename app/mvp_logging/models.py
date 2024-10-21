from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)
from app.behaviour_db import Base
from typing import Optional


class MVPLog(Base):
    __tablename__ = "mvp_log"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    site: Mapped[str] = mapped_column(String)
    action: Mapped[str] = mapped_column(String)
    email: Mapped[Optional[str]] = mapped_column(String)
    detail: Mapped[Optional[str]] = mapped_column(String)

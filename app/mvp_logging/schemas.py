from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class CreateMVPLog(BaseModel):
    site: str
    action: str
    email: Optional[EmailStr] | None = None
    detail: Optional[str] | None = None


class MVPLog(CreateMVPLog):
    id: int
    create_date: datetime

    class ConfigDict:
        from_attributes = True

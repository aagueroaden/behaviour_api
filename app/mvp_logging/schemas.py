from pydantic import BaseModel, EmailStr
from typing import Optional


class CreateMVPLog(BaseModel):
    site: str
    action: str
    email: Optional[EmailStr] | None = None
    detail: Optional[str] | None = None


class MVPLog(CreateMVPLog):
    id: int

    class ConfigDict:
        from_attributes = True

from __future__ import annotations
from pydantic import BaseModel
from typing import List


class CreateSite(BaseModel):
    name: str


class Site(CreateSite):
    id: int
    actions: List[Action]

    class ConfigDict:
        from_attributes = True


class CreateAction(BaseModel):
    name: str
    site_id: int


class Action(CreateAction):
    id: int

    class ConfigDict:
        from_attributes = True


class CreateLog(BaseModel):
    action_id: int
    detail: str


class Log(CreateLog):
    id: int

    class ConfigDict:
        from_attributes = True
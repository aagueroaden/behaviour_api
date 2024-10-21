# here goes all the dependency injections

from app.behaviour_db import behaviour_db
from app.behaviour.service import BehaviourService
from app.mvp_logging.services import MVPLogService
from sqlalchemy.orm import Session
from fastapi import Depends, Header, HTTPException
import os

PUBLIC_API_KEY = os.getenv("API_KEY")


async def validate_public_api_key(api_key: str = Header(...)):
    if api_key != PUBLIC_API_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized API Key")


def get_db() -> Session:
    return next(behaviour_db.get_db())


def get_behaviour_service(db: Session = Depends(get_db)) -> BehaviourService:
    return BehaviourService(db)


def get_mvp_log_service(db: Session = Depends(get_db)) -> MVPLogService:
    return MVPLogService(db)

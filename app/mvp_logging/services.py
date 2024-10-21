from app.mvp_logging.models import MVPLog as DBMVPLog
from app.mvp_logging.schemas import (
    CreateMVPLog,
    MVPLog
)
from sqlalchemy.orm import Session


class MVPLogService:

    def __init__(self, db: Session):
        self.db: Session = db

    def create(self, mvp_log: CreateMVPLog) -> MVPLog:
        db_mvp_log = DBMVPLog(**mvp_log.model_dump(exclude_none=True))
        self.db.add(db_mvp_log)
        self.db.commit()
        self.db.refresh(db_mvp_log)

        return MVPLog(**db_mvp_log.__dict__)

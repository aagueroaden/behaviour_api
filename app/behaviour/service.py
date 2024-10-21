from app.behaviour.models import (
    Action as DBAction,
    Log as DBLog,
    Site as DBSite,
)
from app.behaviour.schemas import (
    Action,
    Log,
    Site,
    CreateAction,
    CreateLog,
    CreateSite,
)
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List


class BehaviourService:

    def __init__(self, db: Session):
        self.db: Session = db

    def create_site(self, site: CreateSite) -> Site:
        existing_site = self.fetch_db_site_by_name(site=site)
        if existing_site:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Site already exist"
            )
        return self.create_db_site(site=site)

    def fetch_db_site_by_name(self, site: CreateSite) -> Site | None:
        """
        Return a site by an exact coincidence of name for a site
        """
        db_site = self.db.query(DBSite).filter(DBSite.name == site.name).first()
        return Site(**db_site.__dict__) if db_site else None

    def create_db_site(self, site: CreateSite) -> Site:
        """
        Create a site in the db
        """
        db_site = DBSite(**site.model_dump(exclude_none=True))
        self.db.add(db_site)
        self.db.commit()
        self.db.refresh(db_site)

        return Site(**db_site.__dict__)

    def get_all_sites(self) -> List[Site]:
        """
        Obtains all the sites
        """
        return self.db.query(DBSite).all()

    def create_action(self, action: CreateAction) -> Action:
        site = self.db.query(DBSite).filter(DBSite.id == action.site_id).first()
        if not site:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Site id {action.site_id} not found",
            )
        existing_action = self.fetch_db_action_by_name_and_site(action=action)
        if existing_action:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Action already exist"
            )
        return self.create_db_action(action=action)

    def fetch_db_action_by_name_and_site(self, action: Action) -> Action | None:
        db_action = self.db.query(DBAction).filter_by(
            name=action.name,
            site_id=action.site_id
        ).first()
        return Action(**db_action.__dict__) if db_action else None

    def create_db_action(self, action: CreateAction) -> Site:
        """
        Create an action in the db
        """
        db_action = DBAction(**action.model_dump(exclude_none=True))
        self.db.add(db_action)
        self.db.commit()
        self.db.refresh(db_action)

        return Action(**db_action.__dict__)

    def get_actions_of_site(self, site_id: int) -> List[Action]:
        return self.db.query(DBAction).filter_by(site_id=site_id).all()

    def get_all_actions(self) -> List[Action]:
        return self.db.query(DBAction).all()

    def create_log(self, log: CreateLog):
        """
        Create a log based on the id of an action
        """
        event = self.db.query(DBAction).filter(DBAction.id == log.action_id).first()

        if not event:
            raise HTTPException(status_code=400, detail=f"Action {log.action_id} not found")

        return self.create_db_log(log=log)

    def create_db_log(self, log: CreateLog):
        """
        Create a log in the DB
        """
        new_log = DBLog(action_id=log.action_id, detail=log.detail)
        self.db.add(new_log)
        self.db.commit()
        self.db.refresh(new_log)

        return Log(**new_log.__dict__)

    def get_log(self, log_id: int):
        log = self.db.query(DBLog).filter(DBLog.id == log_id).first()
        if not log:
            raise HTTPException(status_code=404, detail="Log not found")
        return log

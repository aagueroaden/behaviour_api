from dotenv import load_dotenv
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from tenacity import retry, stop_after_attempt, wait_fixed
import logging
import sys

# Load environment variables from .env file
load_dotenv()


class DatabaseConnection:
    def __init__(self):
        self.BEHAVIOUR_DB_HOST = getenv("BEHAVIOUR_DB_HOST")
        self.BEHAVIOUR_DB_NAME = getenv("BEHAVIOUR_DB_NAME")
        self.BEHAVIOUR_DB_USER = getenv("BEHAVIOUR_DB_USER")
        self.BEHAVIOUR_DB_PASW = getenv("BEHAVIOUR_DB_PASW")
        self.BEHAVIOUR_DB_TYPE = getenv("BEHAVIOUR_DB_TYPE")

        self.DATABASE_URL = f"{self.BEHAVIOUR_DB_TYPE}://{self.BEHAVIOUR_DB_USER}:{self.BEHAVIOUR_DB_PASW}@{self.BEHAVIOUR_DB_HOST}/{self.BEHAVIOUR_DB_NAME}"

        self.engine = None
        self.SessionLocal = None
        self.Base = declarative_base()

        # Initialize the connection when the object is created
        self.initialize()

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(5))
    def _create_engine(self):
        try:
            self.engine = create_engine(
                self.DATABASE_URL,
                connect_args={"connect_timeout": 5},
                pool_pre_ping=True
            )
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            logging.info(f"Connection established with {self.BEHAVIOUR_DB_NAME}")
        except Exception as e:
            logging.error(f"Error creating database engine: {str(e)}")
            raise e

    def initialize(self):
        try:
            self._create_engine()
        except Exception as e:
            logging.error(f"Failed to establish database connection after retries: {str(e)}")
            sys.exit(1)

    @property
    def get_engine(self):
        return self.engine

    @property
    def get_base(self):
        return self.Base

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(5))  # try to reconect 3 times every 5 sec
    def get_db(self) -> Generator[Session, None, None]:
        """Dependency to get the database session."""
        db = self.SessionLocal()
        try:
            yield db
        except Exception as e:
            logging.error(f"Database error: {str(e)}")
            db.rollback()
            raise e
        finally:
            db.close()


# Instantiate the database connection class and expose engine and base MUST BE HERE!

behaviour_db = DatabaseConnection()
engine = behaviour_db.get_engine
Base = behaviour_db.get_base

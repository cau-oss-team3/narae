from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import Config
from app.logger import logger

def setup_database():
    database_url = Config.get_database_url()
    engine = create_engine(database_url)
    logger.info('DB: Connected to database')

    Base.metadata.create_all(bind=engine)
    logger.info('DB: Created tables')

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal

Base = declarative_base()

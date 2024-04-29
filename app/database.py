from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.logger import logger

def setup_database(config):
    database_url = config.get_database_url()
    engine = create_engine(database_url)
    logger.info('DB: Connected to database')

    Base.metadata.create_all(bind=engine)
    logger.info('DB: Created tables')

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal

Base = declarative_base()

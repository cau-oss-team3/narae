import pytest
from unittest.mock import MagicMock, patch

from app.database import setup_database
from app.config import Config

DB_URL = 'sqlite:///:memory:'

@pytest.fixture
def mock_config():
    config = Config()
    config.get_database_url = MagicMock(return_value=DB_URL)
    return config

def test_setup_database(mock_config):
    # 'app.database' scope 내에서 'create_engine', 'sessionmaker' Patch
    with patch('app.database.create_engine') as mock_engine, \
         patch('app.database.sessionmaker') as mock_sessionmaker, \
         patch('app.database.logger') as mock_logger:

        session_local = setup_database(mock_config)

        mock_engine.assert_called_once_with(DB_URL)

        mock_sessionmaker.assert_called_once()
        mock_sessionmaker.assert_called_with(autocommit=False, autoflush=False, bind=mock_engine.return_value)

        assert mock_logger.info.called
        assert session_local == mock_sessionmaker.return_value

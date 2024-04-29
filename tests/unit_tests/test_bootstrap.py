import pytest
from fastapi import FastAPI
from unittest.mock import patch

from app.bootstrap import create_app


@pytest.fixture
def mock_apply_middleware():
    with patch("app.bootstrap.apply_middleware") as mock:
        yield mock

@pytest.fixture
def mock_apply_routes():
    with patch("app.bootstrap.apply_routes") as mock:
        yield mock


def test_create_app():
    app = create_app()

    assert isinstance(app, FastAPI)

    assert app.docs_url == "/docs"
    assert app.openapi_url == "/docs.json"


def test_create_app_with_mocks(mock_apply_middleware, mock_apply_routes):
    create_app()

    mock_apply_middleware.assert_called_once()
    mock_apply_routes.assert_called_once()

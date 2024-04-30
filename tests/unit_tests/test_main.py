from fastapi.responses import RedirectResponse
from app.main import index


def test_index_redirect():
    response = index()
    assert isinstance(response, RedirectResponse)
    assert response.status_code == 307

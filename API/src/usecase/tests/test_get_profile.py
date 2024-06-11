import pytest
from src.errors import UnauthorizedError
from src.usecase.get_profile import get_profile_handler
from chalice import Response
import jwt

SECRET_KEY = "your_secret_key"

@pytest.fixture
def mock_repo(mocker):
    return mocker.patch('src.bootstrap.get_user_repo')

def test_get_profile_success(mock_repo, mocker):
    auth_header = 'Bearer mock_token'
    mock_payload = {
        'user_id': 1
    }
    mock_repo.return_value.get_user_by_id.return_value = (1, 'Test User', 'test@example.com', 'http://example.com/photo.jpg')

    mocker.patch('jwt.decode', return_value=mock_payload)

    response = get_profile_handler(auth_header, SECRET_KEY, mock_repo.return_value)
    assert response.status_code == 200
    response_body = response.body
    assert response_body['name'] == 'Test User'

def test_get_profile_invalid_token(mocker, mock_repo):
    auth_header = 'Bearer invalid_token'
    mocker.patch('jwt.decode', side_effect=jwt.InvalidTokenError)

    try:
        get_profile_handler(auth_header, SECRET_KEY, mock_repo.return_value)
    except UnauthorizedError as e:
        assert str(e) == 'Invalid token'
    else:
        pytest.fail("Expected UnauthorizedError not raised")

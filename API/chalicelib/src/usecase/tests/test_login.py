import pytest
from chalicelib.src.errors import UnauthorizedError
from chalicelib.src.usecase.login import login_handler
from chalice import Response
import jwt

SECRET_KEY = "your_secret_key"

@pytest.fixture
def mock_repo(mocker):
    return mocker.patch('chalicelib.src.bootstrap.get_user_repo')

def test_login_success(mock_repo, mocker):
    data = {
        'email': 'test@example.com',
        'password': 'securepassword'
    }
    mock_repo.return_value.get_user_by_credentials.return_value = (1, 'Test User', 'http://example.com/photo.jpg')

    mocker.patch('jwt.encode', return_value='mock_token')

    response = login_handler(data, mock_repo.return_value)
    assert response.status_code == 200
    response_body = response.body
    assert response_body['token'] == 'mock_token'

def test_login_invalid_credentials(mock_repo):
    data = {
        'email': 'test@example.com',
        'password': 'wrongpassword'
    }
    mock_repo.return_value.get_user_by_credentials.return_value = None

    try:
        login_handler(data, mock_repo.return_value, SECRET_KEY)
    except UnauthorizedError as e:
        assert str(e) == 'Invalid credentials'
    else:
        pytest.fail("Expected UnauthorizedError not raised")

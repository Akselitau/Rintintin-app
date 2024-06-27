import pytest
from chalicelib.src.errors import BadRequestError
from API.chalicelib.src.usecase.create.create_user import create_user_handler
from chalice import Response

@pytest.fixture
def mock_repo(mocker):
    return mocker.patch('chalicelib.src.bootstrap.get_user_repo')

def test_create_user_success(mock_repo):
    data = {
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'securepassword',
        'profile_photo_url': 'http://example.com/photo.jpg'
    }
    mock_repo.return_value.create_user.return_value = 1

    response = create_user_handler(data, mock_repo.return_value)
    assert response.status_code == 201
    response_body = response.body
    assert response_body['message'] == 'User created successfully'

def test_create_user_missing_parameters(mock_repo):
    data = {
        'name': 'Test User',
        'email': 'test@example.com'
    }

    try:
        create_user_handler(data, mock_repo.return_value)
    except BadRequestError as e:
        assert str(e) == 'Missing required parameters'
    else:
        pytest.fail("Expected BadRequestError not raised")

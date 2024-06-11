import pytest
from src.errors import BadRequestError
from src.usecase.create_dog_profile import create_dog_profile_handler

@pytest.fixture
def mock_repo(mocker):
    return mocker.patch('src.bootstrap.get_dog_repo')

import pytest
from src.usecase.create_dog_profile import create_dog_profile_handler
from chalice import Response

@pytest.fixture
def mock_repo(mocker):
    return mocker.patch('src.bootstrap.get_dog_repo')

import pytest
from src.usecase.create_dog_profile import create_dog_profile_handler
from chalice import Response

@pytest.fixture
def mock_repo(mocker):
    return mocker.patch('src.bootstrap.get_dog_repo')

def test_create_dog_profile_success(mock_repo):
    data = {
        'user_id': 1,
        'name': 'Buddy',
        'breed': 'Golden Retriever',
        'profile_photo_url': 'http://example.com/photo.jpg'
    }
    mock_repo.return_value.create_dog_profile.return_value = 1

    response = create_dog_profile_handler(data, mock_repo.return_value)
    assert response.status_code == 201
    response_body = response.body  # Accéder directement au corps de la réponse JSON
    assert response_body['message'] == 'Dog profile created successfully'



def test_create_dog_profile_missing_parameters(mock_repo):
    data = {
        'user_id': 1,
        'name': 'Buddy'
    }

    try:
        create_dog_profile_handler(data, mock_repo.return_value)
    except BadRequestError as e:
        assert str(e) == 'Missing required parameters'
    else:
        pytest.fail("Expected BadRequestError not raised")
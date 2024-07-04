import pytest
from chalice import Response
from chalicelib.src.errors import BadRequestError
from chalicelib.src.usecase.create.create_dog_profile import create_dog_profile_handler

@pytest.fixture
def mock_repo(mocker):
    return mocker.patch('chalicelib.src.bootstrap.get_dog_repo')

def test_create_dog_profile_success_with_birthdate(mock_repo):
    data = {
        'user_id': 1,
        'name': 'Buddy',
        'breed': 'Golden Retriever',
        'profile_photo_url': 'http://example.com/photo.jpg',
        'information': 'Friendly dog',
        'birthdate': '2020-01-01'
    }
    mock_repo.return_value.create_dog_profile.return_value = 1

    response = create_dog_profile_handler(data, mock_repo.return_value)
    assert response.status_code == 201
    response_body = response.body
    assert response_body['message'] == 'Dog profile created successfully'
    assert response_body['dog_id'] == 1

def test_create_dog_profile_success_without_birthdate(mock_repo):
    data = {
        'user_id': 1,
        'name': 'Buddy',
        'breed': 'Golden Retriever',
        'profile_photo_url': 'http://example.com/photo.jpg',
        'information': 'Friendly dog'
    }
    mock_repo.return_value.create_dog_profile.return_value = 1

    response = create_dog_profile_handler(data, mock_repo.return_value)
    assert response.status_code == 201
    response_body = response.body
    assert response_body['message'] == 'Dog profile created successfully'
    assert response_body['dog_id'] == 1

def test_create_dog_profile_missing_parameters(mock_repo):
    data = {
        'user_id': 1,
        'name': 'Buddy'
    }

    with pytest.raises(BadRequestError) as excinfo:
        create_dog_profile_handler(data, mock_repo.return_value)
    
    assert str(excinfo.value) == 'Missing required parameters'

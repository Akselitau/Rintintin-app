import pytest
from chalice import Response
from chalicelib.src.usecase.get.get_dogs_by_user import get_dogs_by_user_handler
from chalicelib.src.application.schema.dog_schema import DogSchema

@pytest.fixture
def mock_repo(mocker):
    # Patcher le module où la fonction est utilisée
    mock = mocker.patch('chalicelib.src.usecase.get.get_dogs_by_user.get_dog_repo')
    return mock

def test_get_dogs_success(mock_repo):
    user_id = 1
    dogs_data = [
        {"dog_id": 1, "user_id": user_id, "name": "Buddy", "breed": "Golden Retriever", "profile_photo_url": "http://example.com/photo.jpg", "information": "Friendly dog", "birthdate": "2020-01-01"},
        {"dog_id": 2, "user_id": user_id, "name": "Max", "breed": "Labrador Retriever", "profile_photo_url": "http://example.com/photo2.jpg", "information": "Playful dog", "birthdate": "2019-05-05"}
    ]
    mock_repo.return_value.get_dogs_by_user.return_value = dogs_data

    expected_dogs_list = DogSchema(many=True).dump(dogs_data)
    response = get_dogs_by_user_handler(user_id)
    
    assert response.status_code == 200
    assert response.body == {"dogs": expected_dogs_list}

def test_get_dogs_empty_list(mock_repo):
    user_id = 1
    mock_repo.return_value.get_dogs_by_user.return_value = []

    response = get_dogs_by_user_handler(user_id)
    
    assert response.status_code == 200
    assert response.body == {"dogs": []}

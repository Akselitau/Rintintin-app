import pytest
from chalice import Response
from chalicelib.src.usecase.get.get_pension_by_id import get_pension_by_id_handler
from unittest.mock import MagicMock

import pytest
from chalice import Response
from chalicelib.src.usecase.get.get_pension_by_id import get_pension_by_id_handler
from unittest.mock import MagicMock

@pytest.fixture
def mock_repo(mocker):
    mock = mocker.patch('chalicelib.src.usecase.get.get_pension_by_id.get_pension_repo')
    return mock

def test_get_pension_by_id_success(mock_repo):
    pension_id = 1
    pension_data = {
        "pension_id": pension_id,
        "user_id": 1,
        "name": "Pension A",
        "address": "123 Main St",
        "phone": "1234567890",
        "email": "pension@example.com",
        "max_capacity": 10,
        "current_occupancy": 5,
        "rating": 4.5,
        "description": "A great place for pets",
        "image_urls": ["http://example.com/photo.jpg"],
        "equipment": ["Beds", "Toys"],
        "hours": {"start": "08:00", "end": "20:00"},
        "night_price": 50.0,
    }

    pension_mock = MagicMock()
    pension_mock.dict.return_value = pension_data
    mock_repo.return_value.get_pension_by_id.return_value = pension_mock

    response = get_pension_by_id_handler(pension_id)
    
    assert response.status_code == 200
    assert response.body == pension_data

def test_get_pension_by_id_not_found(mock_repo):
    pension_id = 1
    mock_repo.return_value.get_pension_by_id.return_value = None

    response = get_pension_by_id_handler(pension_id)
    
    assert response.status_code == 404
    assert response.body == {"message": "Pension not found"}
import pytest
from unittest.mock import patch, MagicMock
from chalicelib.src.usecase.update.update_pension import update_pension_handler
from chalicelib.src.errors import BadRequestError, InternalServerError
from chalicelib.src.domain.Pension import PensionDetail

@pytest.fixture
def mock_pension_repo(mocker):
    return mocker.patch('chalicelib.src.usecase.update.update_pension.get_pension_repo')

def test_update_pension_success(mock_pension_repo):
    mock_repo = mock_pension_repo.return_value
    mock_repo.update_pension.return_value = True

    data = {
        "id": 123,
        "name": "Updated Pension",
        "address": "123 Main St",
        "rating": 4.5,
        "phone": "123-456-7890",
        "email": "pension@test.com",
        "max_capacity": 10,
        "current_occupancy": 5,
        "description": "A nice place",
        "image_urls": ["http://example.com/image1.jpg"],
        "equipment": ["Toys", "Beds"],
        "hours": "Monday to Friday, 9am to 5pm",  # Fix: Correct format for hours
        "night_price": 50
    }

    response = update_pension_handler(data)

    assert response.status_code == 200
    assert response.body == {"message": "Pension status updated successfully"}

def test_update_pension_invalid_parameters(mock_pension_repo):
    data = {
        "id": "pension_123",  # Invalid type
        "name": "Updated Pension",
        "address": "123 Main St",
        "rating": 4.5,
        "phone": "123-456-7890",
        "email": "pension@test.com",
        "max_capacity": 10,
        "current_occupancy": 5,
        "description": "A nice place",
        "image_urls": ["http://example.com/image1.jpg"],
        "equipment": ["Toys", "Beds"],
        "hours": "Monday to Friday, 9am to 5pm",  # Fix: Correct format for hours
        "night_price": 50
    }

    with pytest.raises(BadRequestError, match="Invalid parameters provided"):
        update_pension_handler(data)

def test_update_pension_failure(mock_pension_repo):
    mock_repo = mock_pension_repo.return_value
    mock_repo.update_pension.return_value = False

    data = {
        "id": 123,
        "name": "Updated Pension",
        "address": "123 Main St",
        "rating": 4.5,
        "phone": "123-456-7890",
        "email": "pension@test.com",
        "max_capacity": 10,
        "current_occupancy": 5,
        "description": "A nice place",
        "image_urls": ["http://example.com/image1.jpg"],
        "equipment": ["Toys", "Beds"],
        "hours": "Monday to Friday, 9am to 5pm",  # Fix: Correct format for hours
        "night_price": 50
    }

    with pytest.raises(InternalServerError, match="Failed to update pension status"):
        update_pension_handler(data)

def test_update_pension_internal_server_error(mock_pension_repo):
    mock_repo = mock_pension_repo.return_value
    mock_repo.update_pension.side_effect = Exception("Database error")

    data = {
        "id": 123,
        "name": "Updated Pension",
        "address": "123 Main St",
        "rating": 4.5,
        "phone": "123-456-7890",
        "email": "pension@test.com",
        "max_capacity": 10,
        "current_occupancy": 5,
        "description": "A nice place",
        "image_urls": ["http://example.com/image1.jpg"],
        "equipment": ["Toys", "Beds"],
        "hours": "Monday to Friday, 9am to 5pm",  # Fix: Correct format for hours
        "night_price": 50
    }

    with pytest.raises(InternalServerError, match="An error occurred: Database error"):
        update_pension_handler(data)

import pytest
from datetime import datetime
from unittest.mock import MagicMock, patch
from chalicelib.src.usecase.create.create_reservation import create_reservation_handler
from chalicelib.src.errors import BadRequestError, InternalServerError

@pytest.fixture
def mock_reservation_repo(mocker):
    return mocker.patch('chalicelib.src.bootstrap.get_reservation_repo')

def test_create_reservation_success(mock_reservation_repo):
    mock_repo = mock_reservation_repo.return_value
    mock_repo.make_reservation.return_value = True

    data = {
        "pension_id": "pension_123",
        "check_in": "2024-07-01",
        "check_out": "2024-07-10",
        "dog_id": "dog_123"
    }

    response = create_reservation_handler(data, reservation_repo=mock_repo)
    assert response.status_code == 200
    assert response.body["message"] == "Reservation successful"

def test_create_reservation_missing_parameters(mock_reservation_repo):
    data = {
        "check_in": "2024-07-01",
        "check_out": "2024-07-10",
        "dog_id": "dog_123"
    }

    with pytest.raises(BadRequestError, match="Missing required parameters"):
        create_reservation_handler(data, reservation_repo=mock_reservation_repo.return_value)

def test_create_reservation_invalid_date_format(mock_reservation_repo):
    data = {
        "pension_id": "pension_123",
        "check_in": "invalid-date",
        "check_out": "2024-07-10",
        "dog_id": "dog_123"
    }

    with pytest.raises(BadRequestError, match="Invalid date format"):
        create_reservation_handler(data, reservation_repo=mock_reservation_repo.return_value)

def test_create_reservation_fail_due_to_capacity(mock_reservation_repo):
    mock_repo = mock_reservation_repo.return_value
    mock_repo.make_reservation.return_value = False

    data = {
        "pension_id": "pension_123",
        "check_in": "2024-07-01",
        "check_out": "2024-07-10",
        "dog_id": "dog_123"
    }

    with pytest.raises(BadRequestError, match="Reservation failed due to lack of capacity"):
        create_reservation_handler(data, reservation_repo=mock_repo)

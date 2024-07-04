import pytest
from unittest.mock import MagicMock, patch
from chalice import Response
from chalicelib.src.usecase.get.get_reservations_by_pension import get_reservations_pension_handler
from chalicelib.src.errors import InternalServerError

@pytest.fixture
def mock_reservation_repo(mocker):
    return mocker.patch('chalicelib.src.usecase.get.get_reservations_by_pension.get_reservation_repo')

def test_get_reservations_pension_success(mock_reservation_repo):
    mock_repo = mock_reservation_repo.return_value
    mock_repo.get_reservations_by_pension.return_value = [
        {"reservation_id": "res_123", "pension_id": "pension_123", "check_in": "2024-07-01", "check_out": "2024-07-10"}
    ]

    pension_id = "pension_123"
    response = get_reservations_pension_handler(pension_id)

    assert response.status_code == 200
    assert len(response.body["reservations"]) == 1
    assert response.body["reservations"][0]["reservation_id"] == "res_123"

def test_get_reservations_pension_not_found(mock_reservation_repo):
    mock_repo = mock_reservation_repo.return_value
    mock_repo.get_reservations_by_pension.return_value = []

    pension_id = "pension_123"
    response = get_reservations_pension_handler(pension_id)

    assert response.status_code == 404
    assert response.body["message"] == "Reservations not found"

def test_get_reservations_pension_internal_server_error(mock_reservation_repo):
    mock_repo = mock_reservation_repo.return_value
    mock_repo.get_reservations_by_pension.side_effect = Exception("Database error")

    pension_id = "pension_123"
    with pytest.raises(InternalServerError, match="An error occurred: Database error"):
        get_reservations_pension_handler(pension_id)

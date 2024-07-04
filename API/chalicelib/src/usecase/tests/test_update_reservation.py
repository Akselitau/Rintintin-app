import pytest
from unittest.mock import patch
from chalice import Response
from chalicelib.src.usecase.update.update_reservation import update_reservation_handler
from chalicelib.src.errors import BadRequestError, InternalServerError

@pytest.fixture
def mock_reservation_repo(mocker):
    return mocker.patch('chalicelib.src.usecase.update.update_reservation.get_reservation_repo')

def test_update_reservation_success(mock_reservation_repo):
    mock_repo = mock_reservation_repo.return_value
    mock_repo.update_reservation_status.return_value = True

    data = {
        "reservation_id": "res_123",
        "status": "Accepted"
    }

    response = update_reservation_handler(data)

    assert response.status_code == 200
    assert response.body["message"] == "Reservation status updated successfully"

def test_update_reservation_missing_parameters(mock_reservation_repo):
    data = {
        "reservation_id": "res_123"
    }

    with pytest.raises(BadRequestError, match="Missing required parameters"):
        update_reservation_handler(data)

def test_update_reservation_invalid_status(mock_reservation_repo):
    data = {
        "reservation_id": "res_123",
        "status": "Pending"
    }

    with pytest.raises(BadRequestError, match="Invalid status"):
        update_reservation_handler(data)

def test_update_reservation_failure(mock_reservation_repo):
    mock_repo = mock_reservation_repo.return_value
    mock_repo.update_reservation_status.return_value = False

    data = {
        "reservation_id": "res_123",
        "status": "Accepted"
    }

    with pytest.raises(InternalServerError, match="Failed to update reservation status"):
        update_reservation_handler(data)

def test_update_reservation_internal_server_error(mock_reservation_repo):
    mock_repo = mock_reservation_repo.return_value
    mock_repo.update_reservation_status.side_effect = Exception("Database error")

    data = {
        "reservation_id": "res_123",
        "status": "Accepted"
    }

    with pytest.raises(InternalServerError, match="An error occurred: Database error"):
        update_reservation_handler(data)

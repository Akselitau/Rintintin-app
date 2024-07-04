import pytest
from unittest.mock import patch, MagicMock
from chalice import Response
from chalicelib.src.usecase.get.get_pension_by_id import get_pension_by_id_handler
from chalicelib.src.bootstrap import get_pension_repo

@pytest.fixture
def mock_pension_repo(mocker):
    return mocker.patch('chalicelib.src.usecase.get.get_pension_by_id.get_pension_repo')

def test_get_pension_by_id_success(mock_pension_repo):
    mock_repo = mock_pension_repo.return_value
    mock_pension = MagicMock()
    mock_pension.dict.return_value = {"id": "pension_123", "name": "Pension Test"}
    mock_repo.get_pension_by_id.return_value = mock_pension

    pension_id = "pension_123"
    response = get_pension_by_id_handler(pension_id)

    assert response.status_code == 200
    assert response.body == {"id": "pension_123", "name": "Pension Test"}

def test_get_pension_by_id_not_found(mock_pension_repo):
    mock_repo = mock_pension_repo.return_value
    mock_repo.get_pension_by_id.return_value = None

    pension_id = "pension_123"
    response = get_pension_by_id_handler(pension_id)

    assert response.status_code == 404
    assert response.body == {"message": "Pension not found"}

def test_get_pension_by_id_internal_server_error(mock_pension_repo):
    mock_repo = mock_pension_repo.return_value
    mock_repo.get_pension_by_id.side_effect = Exception("Database error")

    pension_id = "pension_123"
    response = get_pension_by_id_handler(pension_id)

    assert response.status_code == 500
    assert response.body == {"message": "An error occurred: Database error"}

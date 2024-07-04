import pytest
from chalice import Response
from chalicelib.src.usecase.get.get_pensions import get_pensions_handler
from unittest.mock import MagicMock
from chalicelib.src.application.schema.pension_schema import PensionSchema

@pytest.fixture
def mock_repo(mocker):
    return mocker.patch('chalicelib.src.usecase.get.get_pensions.get_pension_repo')

@pytest.fixture
def mock_get_coordinates(mocker):
    return mocker.patch('chalicelib.src.usecase.get.get_pensions.get_coordinates')

@pytest.fixture
def mock_haversine(mocker):
    return mocker.patch('chalicelib.src.usecase.get.get_pensions.haversine')

def test_get_pensions_success_no_address(mock_repo):
    pensions_data = [
        MagicMock(address="123 Main St", rating=4.5),
        MagicMock(address="456 Elm St", rating=4.7)
    ]
    mock_repo.return_value.get_all_pensions.return_value = pensions_data

    query_params = {}
    response = get_pensions_handler(query_params)
    
    assert response.status_code == 200
    assert len(response.body["pensions"]) == 2
    assert response.body["pensions"][0]["rating"] == 4.7
    assert response.body["pensions"][1]["rating"] == 4.5

def test_get_pensions_success_with_address(mock_repo, mock_get_coordinates, mock_haversine):
    pensions_data = [
        MagicMock(address="123 Main St", rating=4.5),
        MagicMock(address="456 Elm St", rating=4.7)
    ]
    mock_repo.return_value.get_all_pensions.return_value = pensions_data
    mock_get_coordinates.side_effect = [(40.7128, -74.0060), (40.730610, -73.935242), (40.741895, -73.989308)]
    mock_haversine.side_effect = [2.0, 1.5]

    query_params = {'address': 'New York, NY'}
    response = get_pensions_handler(query_params)
    
    assert response.status_code == 200
    assert len(response.body["pensions"]) == 2
    assert response.body["pensions"][0]["distance_km"] == 1.5
    assert response.body["pensions"][1]["distance_km"] == 2.0

def test_get_pensions_address_coordinates_failure(mock_repo, mock_get_coordinates):
    pensions_data = [
        MagicMock(address="123 Main St", rating=4.5),
        MagicMock(address="456 Elm St", rating=4.7)
    ]
    mock_repo.return_value.get_all_pensions.return_value = pensions_data
    mock_get_coordinates.side_effect = [None]

    query_params = {'address': 'Unknown Address'}
    response = get_pensions_handler(query_params)
    
    assert response.status_code == 200
    assert len(response.body["pensions"]) == 2
    assert response.body["pensions"][0]["rating"] == 4.7
    assert response.body["pensions"][1]["rating"] == 4.5

def test_get_pensions_empty_list(mock_repo):
    mock_repo.return_value.get_all_pensions.return_value = []

    query_params = {}
    response = get_pensions_handler(query_params)
    
    assert response.status_code == 200
    assert response.body["pensions"] == []
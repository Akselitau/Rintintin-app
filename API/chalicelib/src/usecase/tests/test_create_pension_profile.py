import pytest
from chalice import Response
from chalicelib.src.usecase.create.create_pension_profile import create_pension_profile_handler
from chalicelib.src.errors import BadRequestError
from unittest.mock import MagicMock

@pytest.fixture
def mock_repo(mocker):
    mock = mocker.patch('chalicelib.src.usecase.create.create_pension_profile.get_pension_repo')
    return mock

def test_create_pension_profile_success(mock_repo):
    data = {
        'user_id': 1,
        'name': 'Pension A',
        'address': '123 Main St',
        'phone': '1234567890',
        'email': 'pension@example.com',
        'max_capacity': 10
    }
    mock_repo.return_value.create_pension_profile.return_value = 1

    response = create_pension_profile_handler(data)
    
    assert response.status_code == 201
    assert response.body['message'] == 'Pension profile created successfully'
    assert response.body['pension_id'] == 1

def test_create_pension_profile_missing_parameters(mock_repo):
    data = {
        'user_id': 1,
        'name': 'Pension A'
    }

    with pytest.raises(BadRequestError) as excinfo:
        create_pension_profile_handler(data)
    
    assert str(excinfo.value) == 'Missing required parameters'

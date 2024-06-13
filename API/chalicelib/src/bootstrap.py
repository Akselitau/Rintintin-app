from chalicelib.src.infrastructure.dog_psql_repository import DogPsqlRepository
from chalicelib.src.infrastructure.user_psql_reposiroty import UserPsqlRepository
from chalicelib.src.infrastructure.pension_psql_repository import PsqlPensionRepository
from chalicelib.src.infrastructure.reservation_psql_repository import ReservationPsqlRepository

def get_pension_repo():
    return PsqlPensionRepository()

def get_reservation_repo():
    return ReservationPsqlRepository()

def get_user_repo():
    return UserPsqlRepository()

def get_dog_repo():
    return DogPsqlRepository()


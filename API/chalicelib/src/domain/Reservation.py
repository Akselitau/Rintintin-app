from datetime import datetime

class Reservation:
    def __init__(self, reservation_id: int, dog_id: int, pension_id: int, start_date: datetime, end_date: datetime, status: str):
        self.reservation_id = reservation_id
        self.dog_id = dog_id
        self.pension_id = pension_id
        self.start_date = start_date
        self.end_date = end_date
        self.status = status

    def to_dict(self):
        return {
            "reservation_id": self.reservation_id,
            "dog_id": self.dog_id,
            "pension_id": self.pension_id,
            "start_date": self.start_date.strftime('%Y-%m-%d'),
            "end_date": self.end_date.strftime('%Y-%m-%d'),
            "status": self.status
        }

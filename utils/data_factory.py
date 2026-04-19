import random
import string
from datetime import datetime, timedelta

from models.booking import Booking


class DataFactory:
    """Generates randomised test data to avoid collisions in the shared API environment."""

    @staticmethod
    def random_string(length: int = 8) -> str:
        return "".join(random.choices(string.ascii_letters, k=length))

    @staticmethod
    def random_price(min_val: int = 50, max_val: int = 5000) -> int:
        return random.randint(min_val, max_val)

    @staticmethod
    def random_date_pair(days_ahead_start: int = 30, stay_length: int = 5) -> tuple[str, str]:
        checkin = datetime.now() + timedelta(days=random.randint(1, days_ahead_start))
        checkout = checkin + timedelta(days=random.randint(1, stay_length))
        return checkin.strftime("%Y-%m-%d"), checkout.strftime("%Y-%m-%d")

    @classmethod
    def booking(cls, **overrides) -> dict:
        """Return a valid booking payload dict. Override any field via kwargs."""
        checkin, checkout = cls.random_date_pair()
        b = Booking(
            firstname=overrides.pop("firstname", cls.random_string()),
            lastname=overrides.pop("lastname", cls.random_string()),
            totalprice=overrides.pop("totalprice", cls.random_price()),
            depositpaid=overrides.pop("depositpaid", True),
            bookingdates=overrides.pop(
                "bookingdates", {"checkin": checkin, "checkout": checkout}
            ),
            additionalneeds=overrides.pop("additionalneeds", "Breakfast"),
        )
        data = b.to_dict()
        data.update(overrides)  # apply any remaining custom fields
        return data

from dataclasses import dataclass, asdict, field
from typing import Optional


@dataclass
class BookingDates:
    checkin: str
    checkout: str


@dataclass
class Booking:
    firstname: str
    lastname: str
    totalprice: int
    depositpaid: bool
    bookingdates: dict = field(default_factory=dict)
    additionalneeds: Optional[str] = None

    def to_dict(self) -> dict:
        data = asdict(self)
        # Remove None optional fields
        return {k: v for k, v in data.items() if v is not None}

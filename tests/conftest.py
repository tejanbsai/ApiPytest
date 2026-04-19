import pytest

from api.auth_client import AuthClient
from api.booking_client import BookingClient
from utils.data_factory import DataFactory


@pytest.fixture(scope="session")
def auth_client():
    return AuthClient()


@pytest.fixture(scope="session")
def booking_client():
    return BookingClient()


@pytest.fixture(scope="session")
def auth_token(auth_client):
    """A valid auth token shared across the entire test session."""
    return auth_client.get_valid_token()


@pytest.fixture()
def created_booking(booking_client, auth_token):
    """Create a booking before the test and clean up after."""
    payload = DataFactory.booking()
    resp = booking_client.create_booking(payload)
    data = resp.json()
    booking_id = data["bookingid"]

    yield {"id": booking_id, "payload": payload, "response": data}

    # Cleanup — ignore errors if already deleted by the test
    booking_client.delete_booking(booking_id, token=auth_token)

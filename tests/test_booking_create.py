"""TC-04 to TC-07, TC-19, TC-20 — Booking creation tests."""

import pytest

from utils.data_factory import DataFactory


class TestCreateBooking:

    # TC-04: Create booking with valid data
    @pytest.mark.smoke
    def test_create_booking_valid(self, booking_client, auth_token):
        payload = DataFactory.booking()
        resp = booking_client.create_booking(payload)

        assert resp.status_code == 200
        body = resp.json()
        assert "bookingid" in body
        assert isinstance(body["bookingid"], int)

        booking = body["booking"]
        assert booking["firstname"] == payload["firstname"]
        assert booking["lastname"] == payload["lastname"]
        assert booking["totalprice"] == payload["totalprice"]
        assert booking["depositpaid"] == payload["depositpaid"]
        assert booking["bookingdates"]["checkin"] == payload["bookingdates"]["checkin"]
        assert booking["bookingdates"]["checkout"] == payload["bookingdates"]["checkout"]

        # Cleanup
        booking_client.delete_booking(body["bookingid"], token=auth_token)

    # TC-05: Missing required field (firstname)
    @pytest.mark.negative
    def test_create_booking_missing_firstname(self, booking_client):
        payload = DataFactory.booking()
        del payload["firstname"]
        resp = booking_client.create_booking(payload)

        # API should reject — expect 400 or 500
        assert resp.status_code in (400, 500)

    # TC-06: Invalid data types
    @pytest.mark.negative
    def test_create_booking_invalid_types(self, booking_client):
        payload = DataFactory.booking(totalprice="abc", depositpaid="yes")
        resp = booking_client.create_booking(payload)

        # API should reject or return an error
        assert resp.status_code in (400, 500, 200)
        if resp.status_code == 200:
            # If API coerces values, verify the stored data is sensible
            body = resp.json()
            booking = body.get("booking", {})
            # totalprice should not be the string "abc"
            assert booking.get("totalprice") != "abc"

    # TC-07: Boundary — zero price
    @pytest.mark.boundary
    def test_create_booking_zero_price(self, booking_client, auth_token):
        payload = DataFactory.booking(totalprice=0)
        resp = booking_client.create_booking(payload)

        assert resp.status_code == 200
        body = resp.json()
        assert body["booking"]["totalprice"] == 0

        booking_client.delete_booking(body["bookingid"], token=auth_token)

    # TC-07: Boundary — negative price
    @pytest.mark.boundary
    def test_create_booking_negative_price(self, booking_client, auth_token):
        payload = DataFactory.booking(totalprice=-1)
        resp = booking_client.create_booking(payload)

        # Negative price — document observed behaviour
        if resp.status_code == 200:
            body = resp.json()
            assert body["booking"]["totalprice"] == -1
            booking_client.delete_booking(body["bookingid"], token=auth_token)
        else:
            assert resp.status_code in (400, 500)

    # TC-19: Checkout before checkin (edge case)
    @pytest.mark.boundary
    def test_create_booking_checkout_before_checkin(self, booking_client, auth_token):
        payload = DataFactory.booking(
            bookingdates={"checkin": "2025-12-01", "checkout": "2025-11-01"}
        )
        resp = booking_client.create_booking(payload)

        # Document observed behaviour — API may or may not reject this
        if resp.status_code == 200:
            body = resp.json()
            # Verify dates are stored as sent
            assert body["booking"]["bookingdates"]["checkin"] == "2025-12-01"
            assert body["booking"]["bookingdates"]["checkout"] == "2025-11-01"
            booking_client.delete_booking(body["bookingid"], token=auth_token)
        else:
            assert resp.status_code in (400, 500)

    # TC-20: Very large total price
    @pytest.mark.boundary
    def test_create_booking_large_price(self, booking_client, auth_token):
        payload = DataFactory.booking(totalprice=999999999)
        resp = booking_client.create_booking(payload)

        assert resp.status_code == 200
        body = resp.json()
        assert body["booking"]["totalprice"] == 999999999

        booking_client.delete_booking(body["bookingid"], token=auth_token)

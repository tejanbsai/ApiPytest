"""TC-08 to TC-11 — Booking read / retrieval tests."""

import pytest

from utils.data_factory import DataFactory


class TestReadBooking:

    # TC-08: Get all booking IDs
    @pytest.mark.smoke
    def test_get_all_booking_ids(self, booking_client):
        resp = booking_client.get_booking_ids()

        assert resp.status_code == 200
        body = resp.json()
        assert isinstance(body, list)
        if len(body) > 0:
            assert "bookingid" in body[0]

    # TC-09: Get booking by valid ID
    @pytest.mark.smoke
    def test_get_booking_by_id(self, booking_client, created_booking):
        booking_id = created_booking["id"]
        original = created_booking["payload"]

        resp = booking_client.get_booking(booking_id)

        assert resp.status_code == 200
        body = resp.json()
        assert body["firstname"] == original["firstname"]
        assert body["lastname"] == original["lastname"]
        assert body["totalprice"] == original["totalprice"]
        assert body["depositpaid"] == original["depositpaid"]

    # TC-10: Get booking by non-existent ID
    @pytest.mark.negative
    def test_get_booking_not_found(self, booking_client):
        resp = booking_client.get_booking(9999999)

        assert resp.status_code == 404

    # TC-11: Filter bookings by name
    @pytest.mark.smoke
    def test_filter_bookings_by_name(self, booking_client, created_booking):
        original = created_booking["payload"]
        params = {
            "firstname": original["firstname"],
            "lastname": original["lastname"],
        }
        resp = booking_client.get_booking_ids(params=params)

        assert resp.status_code == 200
        body = resp.json()
        assert isinstance(body, list)
        # The created booking should appear in filtered results
        ids = [item["bookingid"] for item in body]
        assert created_booking["id"] in ids

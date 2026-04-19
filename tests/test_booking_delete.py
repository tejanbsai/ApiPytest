"""TC-16 to TC-18 — Booking deletion tests."""

import pytest

from utils.data_factory import DataFactory


class TestDeleteBooking:

    # TC-16: Delete booking with auth
    @pytest.mark.smoke
    def test_delete_with_auth(self, booking_client, auth_token):
        # Create a booking specifically for deletion
        payload = DataFactory.booking()
        create_resp = booking_client.create_booking(payload)
        booking_id = create_resp.json()["bookingid"]

        resp = booking_client.delete_booking(booking_id, token=auth_token)

        assert resp.status_code == 201

        # Verify booking no longer exists
        get_resp = booking_client.get_booking(booking_id)
        assert get_resp.status_code == 404

    # TC-17: Delete booking without auth — should be rejected
    @pytest.mark.security
    def test_delete_without_auth(self, booking_client, created_booking):
        booking_id = created_booking["id"]

        resp = booking_client.delete_booking_no_auth(booking_id)

        assert resp.status_code == 403

        # Verify booking still exists
        get_resp = booking_client.get_booking(booking_id)
        assert get_resp.status_code == 200

    # TC-18: Delete non-existent booking
    @pytest.mark.negative
    def test_delete_nonexistent_booking(self, booking_client, auth_token):
        resp = booking_client.delete_booking(9999999, token=auth_token)

        assert resp.status_code in (404, 405)

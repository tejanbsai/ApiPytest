"""TC-12 to TC-15 — Booking update tests (PUT and PATCH)."""

import pytest

from utils.data_factory import DataFactory


class TestUpdateBooking:

    # TC-12: Full update with auth
    @pytest.mark.smoke
    def test_full_update_with_auth(self, booking_client, auth_token, created_booking):
        booking_id = created_booking["id"]
        updated_payload = DataFactory.booking()

        resp = booking_client.update_booking(booking_id, updated_payload, token=auth_token)

        assert resp.status_code == 200
        body = resp.json()
        assert body["firstname"] == updated_payload["firstname"]
        assert body["lastname"] == updated_payload["lastname"]
        assert body["totalprice"] == updated_payload["totalprice"]
        assert body["depositpaid"] == updated_payload["depositpaid"]

    # TC-13: Full update without auth — should be rejected
    @pytest.mark.security
    def test_full_update_without_auth(self, booking_client, created_booking):
        booking_id = created_booking["id"]
        original = created_booking["payload"]
        updated_payload = DataFactory.booking()

        resp = booking_client.update_booking_no_auth(booking_id, updated_payload)

        assert resp.status_code == 403

        # Verify booking was NOT modified
        get_resp = booking_client.get_booking(booking_id)
        body = get_resp.json()
        assert body["firstname"] == original["firstname"]

    # TC-14: Partial update (PATCH) with auth
    @pytest.mark.smoke
    def test_partial_update_with_auth(self, booking_client, auth_token, created_booking):
        booking_id = created_booking["id"]
        original = created_booking["payload"]
        patch_data = {"firstname": "UpdatedName"}

        resp = booking_client.partial_update_booking(booking_id, patch_data, token=auth_token)

        assert resp.status_code == 200
        body = resp.json()
        assert body["firstname"] == "UpdatedName"
        # Other fields should remain unchanged
        assert body["lastname"] == original["lastname"]
        assert body["totalprice"] == original["totalprice"]

    # TC-15: Partial update without auth — should be rejected
    @pytest.mark.security
    def test_partial_update_without_auth(self, booking_client, created_booking):
        booking_id = created_booking["id"]
        patch_data = {"firstname": "Hacker"}

        resp = booking_client.partial_update_no_auth(booking_id, patch_data)

        assert resp.status_code == 403

        # Verify booking was NOT modified
        get_resp = booking_client.get_booking(booking_id)
        body = get_resp.json()
        assert body["firstname"] != "Hacker"

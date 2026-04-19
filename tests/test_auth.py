"""TC-01, TC-02, TC-03 — Authentication endpoint tests."""

import pytest


class TestAuth:

    # TC-01: Valid credentials → token issued
    @pytest.mark.smoke
    def test_auth_valid_credentials(self, auth_client):
        resp = auth_client.create_token()

        assert resp.status_code == 200
        body = resp.json()
        assert "token" in body
        assert isinstance(body["token"], str)
        assert len(body["token"]) > 0

    # TC-02: Invalid credentials → no token
    @pytest.mark.negative
    def test_auth_invalid_credentials(self, auth_client):
        resp = auth_client.create_token(username="admin", password="wrongpassword")

        assert resp.status_code == 200
        body = resp.json()
        assert "token" not in body
        assert body.get("reason") == "Bad credentials"

    # TC-03: Missing fields → no token
    @pytest.mark.negative
    def test_auth_missing_fields(self, auth_client):
        resp = auth_client.create_token_raw({})

        body = resp.json()
        assert "token" not in body
        assert body.get("reason") == "Bad credentials"

    # Additional: only username provided
    @pytest.mark.negative
    def test_auth_missing_password(self, auth_client):
        resp = auth_client.create_token_raw({"username": "admin"})

        body = resp.json()
        assert "token" not in body
        assert body.get("reason") == "Bad credentials"

    # Additional: only password provided
    @pytest.mark.negative
    def test_auth_missing_username(self, auth_client):
        resp = auth_client.create_token_raw({"password": "password123"})

        body = resp.json()
        assert "token" not in body
        assert body.get("reason") == "Bad credentials"

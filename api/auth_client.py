import requests

from api.base_client import BaseClient
from config.settings import settings


class AuthClient(BaseClient):
    """Handles authentication against the API."""

    AUTH_PATH = "/auth"

    def create_token(self, username: str = None, password: str = None) -> requests.Response:
        payload = {
            "username": username or settings.AUTH_USERNAME,
            "password": password or settings.AUTH_PASSWORD,
        }
        return self.post(self.AUTH_PATH, json=payload)

    def create_token_raw(self, payload: dict) -> requests.Response:
        """Send arbitrary payload — useful for negative tests."""
        return self.post(self.AUTH_PATH, json=payload)

    def get_valid_token(self) -> str:
        resp = self.create_token()
        return resp.json()["token"]

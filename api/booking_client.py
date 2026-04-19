import requests

from api.base_client import BaseClient


class BookingClient(BaseClient):
    """CRUD operations for the /booking resource."""

    BOOKING_PATH = "/booking"

    # --- Read ---

    def get_booking_ids(self, params: dict = None) -> requests.Response:
        return self.get(self.BOOKING_PATH, params=params)

    def get_booking(self, booking_id: int) -> requests.Response:
        return self.get(f"{self.BOOKING_PATH}/{booking_id}")

    # --- Create ---

    def create_booking(self, payload: dict) -> requests.Response:
        return self.post(self.BOOKING_PATH, json=payload)

    # --- Update ---

    def update_booking(self, booking_id: int, payload: dict, token: str = None) -> requests.Response:
        headers = self._auth_header(token)
        return self.put(f"{self.BOOKING_PATH}/{booking_id}", json=payload, headers=headers)

    def partial_update_booking(self, booking_id: int, payload: dict, token: str = None) -> requests.Response:
        headers = self._auth_header(token)
        return self.patch(f"{self.BOOKING_PATH}/{booking_id}", json=payload, headers=headers)

    # --- Delete ---

    def delete_booking(self, booking_id: int, token: str = None) -> requests.Response:
        headers = self._auth_header(token)
        return self.delete(f"{self.BOOKING_PATH}/{booking_id}", headers=headers)

    # --- Update / Delete without auth (for security tests) ---

    def update_booking_no_auth(self, booking_id: int, payload: dict) -> requests.Response:
        return self.put(f"{self.BOOKING_PATH}/{booking_id}", json=payload)

    def partial_update_no_auth(self, booking_id: int, payload: dict) -> requests.Response:
        return self.patch(f"{self.BOOKING_PATH}/{booking_id}", json=payload)

    def delete_booking_no_auth(self, booking_id: int) -> requests.Response:
        return self.delete(f"{self.BOOKING_PATH}/{booking_id}")

    # --- Helpers ---

    @staticmethod
    def _auth_header(token: str | None) -> dict:
        if token:
            return {"Cookie": f"token={token}"}
        return {}

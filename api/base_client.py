import requests
import logging

from config.settings import settings

logger = logging.getLogger(__name__)


class BaseClient:
    """Generic REST API client — extend for specific resource endpoints."""

    def __init__(self, base_url: str = None):
        self.base_url = (base_url or settings.BASE_URL).rstrip("/")
        self.session = requests.Session()
        self.session.headers.update(settings.DEFAULT_HEADERS)
        self.timeout = settings.REQUEST_TIMEOUT

    # --- Core HTTP verbs ---

    def get(self, path: str, params: dict = None, headers: dict = None) -> requests.Response:
        url = f"{self.base_url}{path}"
        logger.info("GET %s params=%s", url, params)
        resp = self.session.get(url, params=params, headers=headers, timeout=self.timeout)
        logger.info("Response %s: %s", resp.status_code, resp.text[:500])
        return resp

    def post(self, path: str, json: dict = None, headers: dict = None) -> requests.Response:
        url = f"{self.base_url}{path}"
        logger.info("POST %s body=%s", url, json)
        resp = self.session.post(url, json=json, headers=headers, timeout=self.timeout)
        logger.info("Response %s: %s", resp.status_code, resp.text[:500])
        return resp

    def put(self, path: str, json: dict = None, headers: dict = None) -> requests.Response:
        url = f"{self.base_url}{path}"
        logger.info("PUT %s body=%s", url, json)
        resp = self.session.put(url, json=json, headers=headers, timeout=self.timeout)
        logger.info("Response %s: %s", resp.status_code, resp.text[:500])
        return resp

    def patch(self, path: str, json: dict = None, headers: dict = None) -> requests.Response:
        url = f"{self.base_url}{path}"
        logger.info("PATCH %s body=%s", url, json)
        resp = self.session.patch(url, json=json, headers=headers, timeout=self.timeout)
        logger.info("Response %s: %s", resp.status_code, resp.text[:500])
        return resp

    def delete(self, path: str, headers: dict = None) -> requests.Response:
        url = f"{self.base_url}{path}"
        logger.info("DELETE %s", url)
        resp = self.session.delete(url, headers=headers, timeout=self.timeout)
        logger.info("Response %s: %s", resp.status_code, resp.text[:500])
        return resp

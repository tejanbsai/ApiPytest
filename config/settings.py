import os


class Settings:
    """Central configuration — override via environment variables for different environments."""

    BASE_URL: str = os.getenv("API_BASE_URL", "https://restful-booker.herokuapp.com")
    AUTH_USERNAME: str = os.getenv("API_USERNAME", "admin")
    AUTH_PASSWORD: str = os.getenv("API_PASSWORD", "password123")
    REQUEST_TIMEOUT: int = int(os.getenv("API_TIMEOUT", "30"))
    DEFAULT_HEADERS: dict = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


settings = Settings()

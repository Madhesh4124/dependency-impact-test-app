"""HTTP client used by the sample application."""

from dataclasses import dataclass

import requests


@dataclass(frozen=True)
class FetchResult:
    """Small, dependency-independent representation of an HTTP response."""

    url: str
    status_code: int
    content_type: str | None
    body: str


class ApiClient:
    """Fetch JSON resources while exposing common response metadata."""

    def __init__(self, base_url: str, session: requests.Session | None = None) -> None:
        self.base_url = base_url.rstrip("/")
        self.session = session or requests.Session()

    def fetch(self, path: str = "/") -> FetchResult:
        """Fetch a path and capture status, content type, and response text."""
        url = f"{self.base_url}/{path.lstrip('/')}"
        response = self.session.get(url, timeout=5)
        response.raise_for_status()
        return FetchResult(
            url=response.url,
            status_code=response.status_code,
            content_type=response.headers.get("content-type"),
            body=response.text,
        )


def fetch_once(url: str) -> FetchResult:
    """Fetch a URL using requests.get without a persistent session."""
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return FetchResult(
        url=response.url,
        status_code=response.status_code,
        content_type=response.headers.get("content-type"),
        body=response.text,
    )

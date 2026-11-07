from unittest.mock import Mock, patch

import pytest
import requests

from app.client import ApiClient, fetch_once


def response(url: str = "https://example.test/items") -> Mock:
    result = Mock()
    result.url = url
    result.status_code = 200
    result.headers = {"content-type": "application/json"}
    result.text = '{"ok": true}'
    result.raise_for_status.return_value = None
    return result


def test_api_client_uses_session_and_reads_response_metadata() -> None:
    session = Mock()
    session.get.return_value = response()

    result = ApiClient("https://example.test/", session=session).fetch("/items")

    session.get.assert_called_once_with("https://example.test/items", timeout=5)
    assert result.status_code == 200
    assert result.content_type == "application/json"
    assert result.body == '{"ok": true}'


@patch("app.client.requests.get")
def test_fetch_once_uses_requests_get(mock_get: Mock) -> None:
    mock_get.return_value = response("https://example.test/health")

    result = fetch_once("https://example.test/health")

    mock_get.assert_called_once_with("https://example.test/health", timeout=5)
    assert result.url == "https://example.test/health"


def test_api_client_propagates_http_errors() -> None:
    session = Mock()
    failed_response = response()
    failed_response.raise_for_status.side_effect = requests.HTTPError("boom")
    session.get.return_value = failed_response

    with pytest.raises(requests.HTTPError, match="boom"):
        ApiClient("https://example.test", session=session).fetch()

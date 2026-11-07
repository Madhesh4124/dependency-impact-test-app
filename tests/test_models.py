import pytest
from pydantic import ValidationError

from app.models import EndpointConfig, FetchSummary


def test_endpoint_config_strips_name_and_validates_timeout() -> None:
    config = EndpointConfig(name="  catalog ", url="https://example.test", timeout=10)

    assert config.name == "catalog"
    assert config.timeout == 10


def test_endpoint_config_rejects_blank_name() -> None:
    with pytest.raises(ValidationError, match="name must not be blank"):
        EndpointConfig(name=" ", url="https://example.test")


def test_fetch_summary_uses_pydantic_v1_dict_api() -> None:
    summary = FetchSummary(
        endpoint="catalog",
        status_code=200,
        content_type="application/json",
    )

    assert summary.as_dict() == {
        "endpoint": "catalog",
        "status_code": 200,
        "content_type": "application/json",
    }


def test_fetch_summary_forbids_extra_fields() -> None:
    with pytest.raises(ValidationError):
        FetchSummary(
            endpoint="catalog",
            status_code=200,
            content_type=None,
            unexpected=True,
        )

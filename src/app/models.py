"""Pydantic v1 models used by the sample application."""

from pydantic import BaseModel, validator


class EndpointConfig(BaseModel):
    """Configuration for the remote endpoint."""

    name: str
    url: str
    timeout: int = 5

    @validator("name")
    def name_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("name must not be blank")
        return value

    @validator("timeout")
    def timeout_must_be_positive(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("timeout must be positive")
        return value

    class Config:
        anystr_strip_whitespace = True


class FetchSummary(BaseModel):
    """Serializable result summary for CLI output."""

    endpoint: str
    status_code: int
    content_type: str | None

    class Config:
        extra = "forbid"

    def as_dict(self) -> dict[str, object]:
        """Return the Pydantic v1 dictionary representation."""
        return self.dict()

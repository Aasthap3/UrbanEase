from pydantic import BaseModel, Field, field_validator


class LocationSearchParams(BaseModel):
    q: str = Field(min_length=2, max_length=200)
    limit: int = Field(default=5, ge=1, le=10)

    @field_validator('q')
    @classmethod
    def normalize_query(cls, value: str) -> str:
        normalized = value.strip()
        if len(normalized) < 2:
            raise ValueError('Search query must contain at least 2 characters')
        return normalized


class LocationSearchResult(BaseModel):
    id: str | None = None
    name: str
    display_name: str
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    address: dict[str, str] = Field(default_factory=dict)

    @field_validator('latitude', 'longitude', mode='before')
    @classmethod
    def convert_coordinate(cls, value: object) -> float:
        try:
            return float(value)
        except (TypeError, ValueError):
            raise ValueError('Invalid geographic coordinate') from None
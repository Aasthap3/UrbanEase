from pydantic import Field

from app.schemas.urban_score import CategoryScore, UrbanScoreResponse


class PersonalizedScoreResponse(UrbanScoreResponse):
    profile: str
    weight_total: float = Field(ge=99.99, le=100.01)
    categories: list[CategoryScore]
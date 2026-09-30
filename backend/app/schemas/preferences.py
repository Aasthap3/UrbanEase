from math import isclose
from typing import Literal

from pydantic import BaseModel, Field, model_validator

from app.models.amenity import AmenityCategory

ProfileName = Literal['student', 'working_professional', 'family', 'custom']


class PreferenceWeight(BaseModel):
    category: AmenityCategory
    weight: float = Field(ge=0, le=100)


class PreferenceUpdate(BaseModel):
    profile: ProfileName
    weights: list[PreferenceWeight]

    @model_validator(mode='after')
    def validate_weights(self) -> 'PreferenceUpdate':
        categories = [item.category for item in self.weights]
        expected = set(AmenityCategory)
        if len(categories) != len(set(categories)):
            raise ValueError('Each category may appear only once')
        if set(categories) != expected:
            raise ValueError('Weights must include every supported category exactly once')
        if not isclose(sum(item.weight for item in self.weights), 100.0, abs_tol=0.01):
            raise ValueError('Weights must total 100')
        return self


class PreferenceResponse(PreferenceUpdate):
    weight_total: float
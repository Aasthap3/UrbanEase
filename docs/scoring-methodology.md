# Scoring methodology

UrbanEase calculates a baseline accessibility score based on measurable access to nearby amenities. Personalization is outside the current phase.

## Implemented model

- Query stored nearby amenities with PostGIS
- Apply the distance-decay function to each amenity
- Keep the maximum contribution per category
- Apply fixed baseline category weights
- Return an explainable 0-100 score

## Example function

For an amenity at distance `d` meters, the score uses:

S(d) = 1 / (1 + d / 1000)

For each category, `CategoryScore = max(S(d))`. A category with no amenities scores zero. The overall score is the sum of each category score multiplied by its fixed weight. The weights total 100.

The score is a decision-support metric based on selected coordinates, radius, available OpenStreetMap data, and baseline weights. It is not an objective measure of neighborhood quality.

## Personalized MCDA

Authenticated users can replace baseline weights with editable profile or custom weights. Accessibility scores and distance decay remain unchanged:

```text
Personalized Score = Σ(Wᵢ × Sᵢ)
```

Weights are percentages and must total 100. Student, Working Professional, and Family profiles represent example priorities and are editable starting points, not scientifically validated universal importance values.

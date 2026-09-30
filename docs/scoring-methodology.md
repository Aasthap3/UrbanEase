# Scoring methodology

UrbanEase will calculate a personalized accessibility score based on measurable access to amenities and user preferences.

## Planned model

- Measure nearest amenities by category
- Apply a distance-decay function
- Weight categories according to user priorities
- Normalize the final score to a 0-100 scale

## Example function

The current design uses a simple distance decay:

S(d) = 1 / (1 + d)

where d is normalized distance for a category.

This framework can later be replaced or enhanced with Gaussian decay or more geographic weighting.

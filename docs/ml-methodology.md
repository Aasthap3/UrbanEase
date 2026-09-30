# Machine learning methodology

The ML layer is planned to cluster neighborhoods based on measurable geospatial features.

## Candidate features

- grocery_density
- hospital_density
- pharmacy_density
- bank_density
- transport_density
- restaurant_density
- average_amenity_distance
- amenity_diversity

## Planned approach

- Extract neighborhood feature vectors from amenity and distance data
- Run K-means clustering
- Label clusters from observable metrics such as access levels
- Visualize cluster results on the map

This will remain explainable and anchored in measurable features rather than hard-coded judgments.

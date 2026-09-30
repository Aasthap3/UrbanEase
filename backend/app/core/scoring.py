from app.models.amenity import AmenityCategory

SUPPORTED_RADII = frozenset({500, 1000, 2000, 5000})

CATEGORY_WEIGHTS: dict[AmenityCategory, int] = {
    AmenityCategory.GROCERY: 12,
    AmenityCategory.HOSPITAL: 12,
    AmenityCategory.PHARMACY: 10,
    AmenityCategory.BANK: 6,
    AmenityCategory.ATM: 5,
    AmenityCategory.BUS_STOP: 8,
    AmenityCategory.METRO_STATION: 8,
    AmenityCategory.RESTAURANT: 5,
    AmenityCategory.HOTEL: 2,
    AmenityCategory.PETROL_PUMP: 5,
    AmenityCategory.POLICE_STATION: 8,
    AmenityCategory.LAUNDRY: 3,
    AmenityCategory.GYM: 3,
    AmenityCategory.SCHOOL: 7,
    AmenityCategory.COLLEGE: 6,
}

SCORING_CATEGORIES = tuple(CATEGORY_WEIGHTS)

PROFILE_WEIGHTS: dict[str, dict[AmenityCategory, int]] = {
    'student': {
        AmenityCategory.GROCERY: 12,
        AmenityCategory.HOSPITAL: 5,
        AmenityCategory.PHARMACY: 10,
        AmenityCategory.BANK: 3,
        AmenityCategory.ATM: 2,
        AmenityCategory.BUS_STOP: 15,
        AmenityCategory.METRO_STATION: 12,
        AmenityCategory.RESTAURANT: 8,
        AmenityCategory.HOTEL: 1,
        AmenityCategory.PETROL_PUMP: 1,
        AmenityCategory.POLICE_STATION: 1,
        AmenityCategory.LAUNDRY: 1,
        AmenityCategory.GYM: 1,
        AmenityCategory.SCHOOL: 3,
        AmenityCategory.COLLEGE: 25,
    },
    'working_professional': {
        AmenityCategory.GROCERY: 15,
        AmenityCategory.HOSPITAL: 5,
        AmenityCategory.PHARMACY: 10,
        AmenityCategory.BANK: 10,
        AmenityCategory.ATM: 8,
        AmenityCategory.BUS_STOP: 15,
        AmenityCategory.METRO_STATION: 12,
        AmenityCategory.RESTAURANT: 10,
        AmenityCategory.HOTEL: 3,
        AmenityCategory.PETROL_PUMP: 3,
        AmenityCategory.POLICE_STATION: 2,
        AmenityCategory.LAUNDRY: 2,
        AmenityCategory.GYM: 2,
        AmenityCategory.SCHOOL: 1,
        AmenityCategory.COLLEGE: 2,
    },
    'family': {
        AmenityCategory.GROCERY: 18,
        AmenityCategory.HOSPITAL: 18,
        AmenityCategory.PHARMACY: 14,
        AmenityCategory.BANK: 3,
        AmenityCategory.ATM: 2,
        AmenityCategory.BUS_STOP: 10,
        AmenityCategory.METRO_STATION: 4,
        AmenityCategory.RESTAURANT: 3,
        AmenityCategory.HOTEL: 1,
        AmenityCategory.PETROL_PUMP: 2,
        AmenityCategory.POLICE_STATION: 8,
        AmenityCategory.LAUNDRY: 1,
        AmenityCategory.GYM: 1,
        AmenityCategory.SCHOOL: 14,
        AmenityCategory.COLLEGE: 1,
    },
    'custom': dict(CATEGORY_WEIGHTS),
}

if sum(CATEGORY_WEIGHTS.values()) != 100:
    raise RuntimeError('UrbanEase score category weights must total 100')

if any(sum(weights.values()) != 100 or set(weights) != set(SCORING_CATEGORIES) for weights in PROFILE_WEIGHTS.values()):
    raise RuntimeError('Every UrbanEase profile must cover all categories and total 100')
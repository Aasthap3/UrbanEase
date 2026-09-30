from collections.abc import Mapping

from app.models.amenity import AmenityCategory


# Each rule is a set of exact OSM tag values. The order also defines the
# category precedence when an element matches more than one supported rule.
OSM_CATEGORY_RULES: dict[AmenityCategory, tuple[dict[str, str], ...]] = {
    AmenityCategory.GROCERY: (
        {'shop': 'supermarket'},
        {'shop': 'convenience'},
        {'shop': 'grocery'},
        {'amenity': 'marketplace'},
    ),
    AmenityCategory.HOSPITAL: ({'amenity': 'hospital'},),
    AmenityCategory.PHARMACY: ({'amenity': 'pharmacy'},),
    AmenityCategory.BANK: ({'amenity': 'bank'},),
    AmenityCategory.ATM: ({'amenity': 'atm'},),
    AmenityCategory.BUS_STOP: (
        {'highway': 'bus_stop'},
        {'public_transport': 'platform', 'bus': 'yes'},
    ),
    AmenityCategory.METRO_STATION: (
        {'railway': 'station', 'station': 'subway'},
        {'public_transport': 'station', 'subway': 'yes'},
    ),
    AmenityCategory.RESTAURANT: (
        {'amenity': 'restaurant'},
        {'amenity': 'fast_food'},
        {'amenity': 'cafe'},
    ),
    AmenityCategory.HOTEL: (
        {'tourism': 'hotel'},
        {'tourism': 'hostel'},
        {'tourism': 'motel'},
        {'tourism': 'guest_house'},
    ),
    AmenityCategory.PETROL_PUMP: ({'amenity': 'fuel'},),
    AmenityCategory.POLICE_STATION: ({'amenity': 'police'},),
    AmenityCategory.LAUNDRY: ({'shop': 'laundry'}, {'amenity': 'laundry'}),
    AmenityCategory.GYM: ({'leisure': 'fitness_centre'}, {'amenity': 'gym'}),
    AmenityCategory.SCHOOL: ({'amenity': 'school'},),
    AmenityCategory.COLLEGE: (
        {'amenity': 'college'},
        {'amenity': 'university'},
    ),
}


def rule_matches(tags: Mapping[str, object], rule: Mapping[str, str]) -> bool:
    return all(tags.get(key) == value for key, value in rule.items())


def category_for_tags(
    tags: Mapping[str, object],
    requested_category: AmenityCategory | None = None,
) -> AmenityCategory | None:
    categories = (requested_category,) if requested_category is not None else OSM_CATEGORY_RULES
    for category in categories:
        if any(rule_matches(tags, rule) for rule in OSM_CATEGORY_RULES[category]):
            return category
    return None


def overpass_selectors(category: AmenityCategory | None = None) -> list[dict[str, str]]:
    categories = (category,) if category is not None else tuple(OSM_CATEGORY_RULES)
    selectors: list[dict[str, str]] = []
    for selected_category in categories:
        selectors.extend(OSM_CATEGORY_RULES[selected_category])
    return selectors
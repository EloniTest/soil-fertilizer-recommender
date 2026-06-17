from database import get_crop_data, get_fertilizer_by_elem


# Dictionaries and reference books for interpreting calculations
DEFICIT_LEVELS = {
    1: "небольшой дефицит",
    2: "умеренный дефицит",
    3: "острый дефицит"
}

# Basic doses of pure active ingredient (кг д.в/га) depending on the level of deficiency [1, 2, 3]
BASE_DOSES = {
    "N": [40, 70, 120],
    "P": [45, 80, 130],
    "K": [50, 90, 140]
}
# determination of the level of deficit
def determine_deficit_level(fact_value, opt_min):

    gap_percentage = ((opt_min - fact_value) / opt_min) * 100
    if gap_percentage <= 20.0:
        # Minor deficit (up to 20%)
        return 1
    elif gap_percentage <= 45.0:
        # Moderate deficiency (deviation from 20% to 45%)
        return 2
    else:
        # strong deficiency (deviation more than 45%)
        return 3 
    

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
    
def calculate_fertilizer_dose(element, deficit_level, crop_coefficient):
    base_dose_dv = BASE_DOSES[element][deficit_level - 1]
    final_dose_dv = base_dose_dv * crop_coefficient
    fert_name, content_pct, method, notes = get_fertilizer_by_elem(element)
    dose_physical = round((final_dose_dv / content_pct) * 100, 1)
    return {
        "element": element,
        "status": DEFICIT_LEVELS[deficit_level],
        "fert_name": fert_name,
        "dose_phys": dose_physical,
        "method": method,
        "notes": notes
    }

def calculate_recommendation(crop_name, fact_n, fact_p, fact_k, fact_ph):
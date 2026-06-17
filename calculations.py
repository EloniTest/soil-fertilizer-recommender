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
    crop_norms = get_crop_data(crop_name)
    if not crop_norms:
        return None
    (crop_id, 
     n_min, n_max, 
     p_min, p_max, 
     k_min, k_max, 
     ph_min, ph_max, 
     coeff_n, coeff_p, coeff_k) = crop_norms
    
    report = {
        "norms": (n_min, n_max, p_min, p_max, k_min, k_max, ph_min, ph_max),
        "fertilizers": [],
        "lime": None
    }

    elements_to_check = [
        ("N", fact_n, n_min, coeff_n),
        ("P", fact_p, p_min, coeff_p),
        ("K", fact_k, k_min, coeff_k)
    ]

    for element, fact_value, opt_min, crop_coefficient in elements_to_check:
        # if the actual value in the soil is higher than or equal to the minimum, there is no deficiency
        if fact_value >= opt_min:
            continue
            
        # launch a chain of calculations: deficit level -> fertilizer weight
        deficit_level = determine_deficit_level(fact_value, opt_min)
        fertilizer_data = calculate_fertilizer_dose(element, deficit_level, crop_coefficient)
        
        # Adding a position to the final report
        report["fertilizers"].append(fertilizer_data)
        
    if fact_ph < ph_min:
        # calculate the difference between the norm and the fact
        gap_ph = ph_min - fact_ph
        
        # agronomic rule: every 0.1 pH deficit requires 0.8 tons of lime per hectare
        lime_dose_tons = round((gap_ph / 0.1) * 0.8, 1)
        
        # obtain the ameliorant data from the database
        lime_name, _, method, notes = get_fertilizer_by_elem("lime")
        
        report["lime"] = {
            "dose": lime_dose_tons,
            "name": lime_name,
            "method": method,
            "notes": notes
        }
        
    return report


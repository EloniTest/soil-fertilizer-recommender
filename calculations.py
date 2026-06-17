from database import get_crop_data, get_fertilizer_by_elem


LEVEL_LABELS = {1: "небольшой дефицит", 2: "умеренный дефицит", 3: "острый дефицит"}
BASE_DOSES = {"N": [40, 70, 120], "P": [45, 80, 130], "K": [50, 90, 140]}

def calculate_recommendation(crop_name, n, p, k, ph):
    # Extracting norms from SQLite
    raw_data = get_crop_data(crop_name)
    if not raw_data:
        return 0
        
    _, n_min, n_max, p_min, p_max, k_min, k_max, ph_min, ph_max, c_n, c_p, c_k = raw_data
    
    result = {
        "norms": (n_min, n_max, p_min, p_max, k_min, k_max, ph_min, ph_max),
        "fertilizers": [],
        "lime": None
    }
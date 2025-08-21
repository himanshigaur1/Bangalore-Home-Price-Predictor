import json
import pickle
import numpy as np
from difflib import get_close_matches  # fuzzy match for unknown locations

__locations = None
__data_columns = None
__model = None

def get_estimated_price(total_sqft, location, bhk, bath):
    location_input = location.lower().strip()

    try:
        loc_index = __data_columns.index(location_input)
    except ValueError:
        # 🔹 fuzzy match for unknown locations
        matches = get_close_matches(location_input, __data_columns[3:], n=1, cutoff=0.6)
        if matches:
            loc_index = __data_columns.index(matches[0])
            print(f"⚠️ Using closest match '{matches[0]}' for location '{location}'")
        else:
            loc_index = -1
            print(f"⚠️ Location '{location}' not found, using default vector")

    x = np.zeros(len(__data_columns))
    x[0] = total_sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1

    try:
        return round(__model.predict([x])[0], 2)
    except Exception as e:
        print("❌ Model prediction failed:", e)
        return 0

def get_location_names():
    return __locations

def load_saved_artifacts():
    global __locations, __data_columns, __model
    print("Loading artifacts...")

    try:
        with open("./artifacts/columns.json", 'r') as f:
            __data_columns = json.load(f)['data_columns']
            __locations = __data_columns[3:]
            print("✅ Columns loaded. Example locations:", __locations[:5])
    except Exception as e:
        print("❌ Failed to load columns.json:", e)

    try:
        with open("./artifacts/bangalore_home_prices_model.pickle", 'rb') as f:
            __model = pickle.load(f)
            print("✅ Model loaded successfully.")
    except Exception as e:
        print("❌ Failed to load model:", e)

    print("Artifacts loading done.")

"""Pet walking service input processors.

Lab 7 fixed version - Pradyumn Bidari (PES1UG24AM194).
"""

import math


def parse_walk_schedule(schedule_spec):
    """Return the walk price or an error message for malformed schedules.

    Expected format: "<positive pet count>-<positive minutes>-YES|NO".
    """
    if not isinstance(schedule_spec, str):
        return "Invalid walk schedule"

    parts = schedule_spec.strip().split("-")
    if len(parts) != 3:
        return "Invalid walk schedule"

    pets_str, mins_str, weekend_str = (part.strip() for part in parts)
    if not pets_str or not mins_str:
        return "Invalid walk schedule"

    weekend_fee = {"YES": 15.0, "NO": 0.0}.get(weekend_str.upper())
    if weekend_fee is None:
        return "Invalid walk schedule"

    try:
        pets = int(pets_str)
        mins = int(mins_str)
        if pets <= 0 or mins <= 0:
            return "Invalid walk schedule"
        base_fee = 20.0 if mins <= 30 else 35.0
        total = base_fee + (pets * 5.0) + weekend_fee
        if not math.isfinite(total):
            return "Invalid walk schedule"
    except (ValueError, OverflowError):
        return "Invalid walk schedule"

    return f"Walk: {pets} pets, {mins} mins - Total ${total:.2f}"

def compute_pace_per_pet(walk_metrics_str):
    """Return finite minutes per pet, or None for invalid/unsafe input."""
    if not isinstance(walk_metrics_str, str):
        return None

    parts = walk_metrics_str.split("/")
    if len(parts) != 2:
        return None

    try:
        mins, pets = (float(part.strip()) for part in parts)
        if not (math.isfinite(mins) and math.isfinite(pets)):
            return None
        if mins <= 0 or pets <= 0:
            return None
        pace = mins / pets
        if not math.isfinite(pace):
            return None
        return round(pace, 2)
    except (ValueError, OverflowError, ZeroDivisionError):
        return None

def lookup_temperament_surcharge(temperament_code):
    """Return the fee for a recognized temperament, otherwise None."""
    if not isinstance(temperament_code, str):
        return None

    code = temperament_code.strip().upper()
    surcharges = {
        "CAL": 0.0,
        "CALM": 0.0,
        "PLY": 5.0,
        "PLAYFUL": 5.0,
        "REA": 12.0,
        "REACTIVE": 12.0,
        "AGG": 20.0,
        "AGGRESSIVE": 20.0,
    }
    return surcharges.get(code)

def main():
    print("==== Running parse_walk_schedule ====")
    s_input = input("Enter schedule (e.g. 2-30-YES): ")
    print(parse_walk_schedule(s_input))

    print("\n==== Running compute_pace_per_pet ====")
    p_input = input("Enter minutes/pets (e.g. 45/3): ")
    pace = compute_pace_per_pet(p_input)
    print("Pace (min/pet):", pace if pace is not None else "Invalid pace input")

    print("\n==== Running lookup_temperament_surcharge ====")
    t_input = input("Enter temperament code (e.g. CALM, PLAYFUL, AGGRESSIVE): ")
    surcharge = lookup_temperament_surcharge(t_input)
    if surcharge is None:
        print("Invalid temperament code")
    else:
        print(f"Surcharge: ${surcharge:.2f}")

if __name__ == "__main__":
    main()


"""Manage pharmacy stock, patient records, and prescriptions."""

import json
import sqlite3
from datetime import datetime
from pathlib import Path

# Global state
conn = sqlite3.connect(":memory:")
stock = {}
prescriptions = []


def setup_database():
    """Create and populate the patient database."""
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE patients (id TEXT, name TEXT, allergy TEXT)"
    )
    cur.executemany(
        "INSERT INTO patients VALUES (?, ?, ?)",
        [
            ("P1", "Kavya", "penicillin"),
            ("P2", "Arjun", "none"),
            ("P3", "Meena", "ibuprofen"),
        ],
    )
    conn.commit()


def find_patient(name):
    """Find a patient by name using a parameterized SQL query."""
    cur = conn.cursor()
    query = "SELECT id, allergy FROM patients WHERE name = ?"
    return cur.execute(query, (name,)).fetchall()


def add_stock(drug, units, expiry, batch_log=None):
    """Add drug units to stock and optionally record the batch."""
    if batch_log is None:
        batch_log = []

    if units <= 0:
        raise ValueError("Units added must be greater than zero.")

    datetime.strptime(expiry, "%Y-%m-%d")

    current_stock = stock.get(drug, {})
    stock[drug] = {
        "units": current_stock.get("units", 0) + units,
        "expiry": expiry,
    }
    batch_log.append((drug, units))
    return len(batch_log)


def dispense(patient_name, drug, units):
    """Dispense medication when patient, allergy, and stock checks pass."""
    if units <= 0:
        print("Dispense error: units must be positive.")
        return False

    try:
        patients = find_patient(patient_name)
        if not patients:
            print("Dispense error: patient not found.")
            return False

        patient_id, allergy = patients[0]
        drug_name = drug.casefold()
        allergy_name = allergy.casefold()

        if allergy_name != "none" and allergy_name in drug_name:
            print("Allergy warning for", patient_name)
            return False

        matching_drug = next(
            (name for name in stock if name.casefold() == drug_name),
            None,
        )
        if matching_drug is None:
            print("Dispense error: drug not found in stock.")
            return False

        if stock[matching_drug]["units"] < units:
            print("Dispense error: insufficient stock.")
            return False

        stock[matching_drug]["units"] -= units
        prescriptions.append(
            {
                "patient": patient_id,
                "drug": matching_drug,
                "units": units,
                "time": datetime.now().isoformat(timespec="seconds"),
            }
        )
        return True

    except (sqlite3.Error, TypeError, ValueError) as error:
        print("Dispense error:", error)
        return False


def expiring_soon(days=30):
    """Return drugs expiring within the specified number of days."""
    if days < 0:
        raise ValueError("Days must not be negative.")

    soon = []
    today = datetime.now()

    for drug, details in stock.items():
        expiry = datetime.strptime(details["expiry"], "%Y-%m-%d")
        remaining_days = (expiry.date() - today.date()).days

        if 0 <= remaining_days <= days:
            soon.append(drug)

    return soon


def export_prescriptions(file="prescriptions.json"):
    """Export prescription records to a JSON file."""
    output_path = Path(file)
    with output_path.open("w", encoding="utf-8") as output_file:
        json.dump(prescriptions, output_file, indent=4)


def load_stock(file="stock.json"):
    """Load stock records from JSON when the file exists."""
    global stock

    input_path = Path(file)
    if not input_path.exists():
        return

    try:
        with input_path.open("r", encoding="utf-8") as input_file:
            loaded_stock = json.load(input_file)

        if not isinstance(loaded_stock, dict):
            raise ValueError("Stock data must be a JSON object.")

        for drug, details in loaded_stock.items():
            if (
                not isinstance(drug, str)
                or not isinstance(details, dict)
                or not isinstance(details.get("units"), int)
                or isinstance(details.get("units"), bool)
                or details["units"] < 0
                or not isinstance(details.get("expiry"), str)
            ):
                raise ValueError(f"Invalid stock record for {drug!r}.")

            datetime.strptime(details["expiry"], "%Y-%m-%d")

        stock = loaded_stock

    except (OSError, json.JSONDecodeError, ValueError) as error:
        print("Unable to load stock:", error)


def print_stock():
    """Display all drugs and their available units."""
    print("Pharmacy Stock")
    for drug, details in stock.items():
        print(
            f"{drug} -> {details['units']} units, "
            f"expires {details['expiry']}"
        )


def main():
    """Run the pharmacy stock management demonstration."""
    setup_database()
    load_stock()

    add_stock("Paracetamol", 100, "2027-03-01")
    add_stock("Amoxicillin", 20, "2027-12-31")
    add_stock("Penicillin", 50, "2027-01-15")
    add_stock("Ibuprofen", 15, "2026-11-30")

    print(
        "Arjun gets Amoxicillin:",
        dispense("Arjun", "Amoxicillin", 30),
    )
    print(
        "Kavya gets Penicillin:",
        dispense("Kavya", "Penicillin", 10),
    )
    print(
        "Meena gets ibuprofen:",
        dispense("Meena", "ibuprofen", 2),
    )
    print("Unknown patient:", dispense("Ghost", "Paracetamol", 5))

    name = input("Patient name to look up (Enter for Arjun): ") or "Arjun"
    print("Lookup result:", find_patient(name))
    print("Expiring within 30 days:", expiring_soon())
    export_prescriptions()
    print_stock()


if __name__ == "__main__":
    main()

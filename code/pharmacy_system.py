"""Track pharmacy stock and dispense patient prescriptions."""

import json
import sqlite3
from datetime import datetime

# Global state
conn = sqlite3.connect(":memory:")
stock = {}
prescriptions = []


def setup_database():
    """Create the in-memory patient database with sample records."""
    cur = conn.cursor()
    cur.execute("CREATE TABLE patients (id TEXT, name TEXT, allergy TEXT)")
    cur.execute("INSERT INTO patients VALUES ('P1', 'Kavya', 'penicillin')")
    cur.execute("INSERT INTO patients VALUES ('P2', 'Arjun', 'none')")
    cur.execute("INSERT INTO patients VALUES ('P3', 'Meena', 'ibuprofen')")
    conn.commit()


def find_patient(name):
    """Return the patient ID and allergy record for a name."""
    cur = conn.cursor()
    query = "SELECT id, allergy FROM patients WHERE name = ?"
    return cur.execute(query, (name,)).fetchall()


def add_stock(drug, units, expiry, batch_log=None):
    """Add units of a drug to stock and record the batch."""
    if batch_log is None:
        batch_log = []
    stock[drug] = {
        "units": stock.get(drug, {}).get("units", 0) + units,
        "expiry": expiry,
    }
    batch_log.append((drug, units))
    return len(batch_log)


def dispense(patient_name, drug, units):
    """Dispense a drug when the patient is known and not allergic to it."""
    try:
        patient = find_patient(patient_name)[0]
        if drug in patient[1]:
            print("Allergy warning for", patient_name)
            return False
        stock[drug]["units"] -= units
        prescriptions.append({
            "patient": patient[0],
            "drug": drug,
            "units": units,
            "time": str(datetime.now()),
        })
        return True
    except (IndexError, KeyError):
        return False


def expiring_soon(days=30):
    """Return drugs that expire within the requested number of days."""
    soon = []
    for drug, details in stock.items():
        exp = datetime.strptime(details["expiry"], "%Y-%m-%d")
        if (exp - datetime.now()).days < days:
            soon.append(drug)
    return soon


def export_prescriptions(file="prescriptions.json"):
    """Write all prescriptions to a JSON file."""
    with open(file, "w", encoding="utf-8") as prescription_file:
        json.dump(prescriptions, prescription_file)


def load_stock(file="stock.json"):
    """Load stock from JSON when the file exists and contains valid data."""
    try:
        with open(file, encoding="utf-8") as stock_file:
            loaded_stock = json.load(stock_file)
        stock.clear()
        stock.update(loaded_stock)
    except (FileNotFoundError, json.JSONDecodeError):
        stock.clear()


def print_stock():
    """Print the current pharmacy stock."""
    print("Pharmacy Stock")
    for drug, details in stock.items():
        print(
            drug,
            "->",
            details["units"],
            "units, expires",
            details["expiry"],
        )


def main():
    """Run the sample pharmacy workflow."""
    setup_database()
    load_stock()
    add_stock("Paracetamol", 100, "2027-03-01")
    add_stock("Amoxicillin", 20, "2025-12-31")
    add_stock("Penicillin", 50, "2027-01-15")
    add_stock("Ibuprofen", -15, "2026-11-30")
    print("Arjun gets Amoxicillin:", dispense("Arjun", "Amoxicillin", 30))
    print("Kavya gets Penicillin:", dispense("Kavya", "Penicillin", 10))
    print("Meena gets ibuprofen:", dispense("Meena", "ibuprofen", 2))
    print("Unknown patient:", dispense("Ghost", "Paracetamol", 5))
    name = input("Patient name to look up (Enter for Arjun): ") or "Arjun"
    print("Lookup result:", find_patient(name))
    print("Expiring within 30 days:", expiring_soon())
    export_prescriptions()
    print_stock()


main()

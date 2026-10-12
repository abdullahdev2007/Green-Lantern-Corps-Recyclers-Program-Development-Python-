"""
============================================================
Green Lantern Corps Recyclers
Automated E-Waste Management System (AEWMS)
============================================================
Module  : CSE4202 – Fundamentals in Programming
Author  : Student
Version : 1.0
============================================================
"""

import json
import os
from datetime import datetime, timedelta

# ─────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────
DATA_FILE = "ewaste_data.json"
STORAGE_CAPACITY = 1000          # Maximum storage in kg
STORAGE_WARNING_THRESHOLD = 0.80 # 80 % triggers a warning
BULK_DISCOUNT_THRESHOLD = 50     # kg above which 5 % discount applies
BULK_DISCOUNT_RATE = 0.05
HAZARD_DAYS_LIMIT = 30           # Days before hazardous item alert
VALID_CATEGORIES = ["Recyclable", "Hazardous", "Non-Recyclable"]
VALID_STATUSES   = ["Stored", "Recycled", "Disposed"]


# ─────────────────────────────────────────────
# Data Persistence
# ─────────────────────────────────────────────

def load_data():
    """
    Load e-waste records from a JSON file.

    Returns:
        list: A list of e-waste item dictionaries.  Returns a default
              sample dataset when no saved file exists.
    """
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)

    # Default sample data for demonstration
    today = datetime.today()
    sample = [
        {
            "id": "EW001",
            "device_name": "Laptop",
            "category": "Recyclable",
            "weight": 2.5,
            "fee_per_kg": 150.0,
            "storage_status": "Stored",
            "date_added": today.strftime("%Y-%m-%d")
        },
        {
            "id": "EW002",
            "device_name": "Mobile Phone",
            "category": "Hazardous",
            "weight": 0.3,
            "fee_per_kg": 200.0,
            "storage_status": "Stored",
            "date_added": (today - timedelta(days=35)).strftime("%Y-%m-%d")
        },
        {
            "id": "EW003",
            "device_name": "Printer",
            "category": "Non-Recyclable",
            "weight": 8.0,
            "fee_per_kg": 100.0,
            "storage_status": "Stored",
            "date_added": today.strftime("%Y-%m-%d")
        },
        {
            "id": "EW004",
            "device_name": "CRT Monitor",
            "category": "Hazardous",
            "weight": 15.0,
            "fee_per_kg": 250.0,
            "storage_status": "Recycled",
            "date_added": (today - timedelta(days=10)).strftime("%Y-%m-%d")
        },
        {
            "id": "EW005",
            "device_name": "Desktop PC",
            "category": "Recyclable",
            "weight": 12.0,
            "fee_per_kg": 130.0,
            "storage_status": "Stored",
            "date_added": today.strftime("%Y-%m-%d")
        },
    ]
    return sample


def save_data(items):
    """
    Persist e-waste records to a JSON file.

    Args:
        items (list): The list of e-waste item dictionaries to save.
    """
    with open(DATA_FILE, "w") as file:
        json.dump(items, file, indent=4)
    print("\n  [OK] Data saved successfully.")


# ─────────────────────────────────────────────
# Display
# ─────────────────────────────────────────────

def display_items(items):
    """
    Display all e-waste items in a formatted table.

    Args:
        items (list): List of e-waste item dictionaries.
    """
    if not items:
        print("\n  No e-waste records found.")
        return

    header = (
        f"\n{'─'*110}\n"
        f"  {'ID':<8} {'Device Name':<20} {'Category':<18} "
        f"{'Weight(kg)':<12} {'Fee/kg(LKR)':<14} {'Status':<12} {'Date Added'}\n"
        f"{'─'*110}"
    )
    print(header)
    for item in items:
        print(
            f"  {item['id']:<8} {item['device_name']:<20} {item['category']:<18} "
            f"{item['weight']:<12.2f} {item['fee_per_kg']:<14.2f} "
            f"{item['storage_status']:<12} {item['date_added']}"
        )
    print(f"{'─'*110}")
    print(f"  Total items: {len(items)}")


# ─────────────────────────────────────────────
# Waste Collection Management
# ─────────────────────────────────────────────

def generate_id(items):
    """
    Auto-generate the next sequential e-waste item ID.

    Args:
        items (list): Existing item list used to determine the next ID number.

    Returns:
        str: A zero-padded ID string in the form EWxxx.
    """
    if not items:
        return "EW001"
    ids = [int(item["id"][2:]) for item in items if item["id"].startswith("EW")]
    return f"EW{max(ids) + 1:03d}"


def get_total_stored_weight(items):
    """
    Calculate total weight of items currently in Stored status.

    Args:
        items (list): List of all e-waste item dictionaries.

    Returns:
        float: Combined weight (kg) of stored items.
    """
    return sum(item["weight"] for item in items if item["storage_status"] == "Stored")


def add_item(items):
    """
    Interactively add a new e-waste item with full input validation.

    Prevents additions when storage capacity is full.

    Args:
        items (list): The current list of e-waste items (modified in place).
    """
    print("\n  ── Add New E-Waste Item ──")

    # Storage full check
    current_weight = get_total_stored_weight(items)
    if current_weight >= STORAGE_CAPACITY:
        print(f"\n  [ALERT] Storage is full ({current_weight:.1f} kg / {STORAGE_CAPACITY} kg). "
              "Cannot add new item.")
        return

    # Device name
    device_name = input("  Enter Device Name: ").strip()
    if not device_name:
        print("  [ERROR] Device name cannot be empty.")
        return

    # Category selection
    print("  Categories: " + " | ".join(VALID_CATEGORIES))
    category = input("  Enter Category: ").strip().title()
    if category not in VALID_CATEGORIES:
        print(f"  [ERROR] Invalid category. Choose from: {', '.join(VALID_CATEGORIES)}")
        return

    # Weight validation
    try:
        weight = float(input("  Enter Weight (kg): "))
        if weight <= 0:
            print("  [ERROR] Weight must be a positive number.")
            return
    except ValueError:
        print("  [ERROR] Invalid weight. Please enter a numeric value.")
        return

    # Fee per kg validation
    try:
        fee_per_kg = float(input("  Enter Recycling Fee per kg (LKR): "))
        if fee_per_kg < 0:
            print("  [ERROR] Fee cannot be negative.")
            return
    except ValueError:
        print("  [ERROR] Invalid fee. Please enter a numeric value.")
        return

    # Capacity check after weight entry
    if current_weight + weight > STORAGE_CAPACITY:
        available = STORAGE_CAPACITY - current_weight
        print(f"  [ERROR] Adding {weight} kg exceeds capacity. "
              f"Only {available:.2f} kg space remaining.")
        return

    new_item = {
        "id": generate_id(items),
        "device_name": device_name,
        "category": category,
        "weight": weight,
        "fee_per_kg": fee_per_kg,
        "storage_status": "Stored",
        "date_added": datetime.today().strftime("%Y-%m-%d")
    }
    items.append(new_item)
    print(f"\n  [OK] Item '{device_name}' added successfully with ID {new_item['id']}.")


def update_item(items):
    """
    Update the weight of an existing e-waste item by its ID.

    Args:
        items (list): The current list of e-waste items (modified in place).
    """
    print("\n  ── Update Item Weight ──")
    item_id = input("  Enter Item ID to update: ").strip().upper()
    target = next((i for i in items if i["id"] == item_id), None)

    if not target:
        print(f"  [ERROR] Item ID '{item_id}' not found.")
        return

    print(f"  Current Weight: {target['weight']} kg")
    try:
        new_weight = float(input("  Enter New Weight (kg): "))
        if new_weight <= 0:
            print("  [ERROR] Weight must be a positive number.")
            return
    except ValueError:
        print("  [ERROR] Invalid input. Please enter a numeric value.")
        return

    target["weight"] = new_weight
    print(f"  [OK] Weight updated to {new_weight} kg for item {item_id}.")


def delete_item(items):
    """
    Remove an e-waste item from the system by its ID.

    Args:
        items (list): The current list of e-waste items (modified in place).
    """
    print("\n  ── Delete E-Waste Item ──")
    item_id = input("  Enter Item ID to delete: ").strip().upper()
    target = next((i for i in items if i["id"] == item_id), None)

    if not target:
        print(f"  [ERROR] Item ID '{item_id}' not found.")
        return

    confirm = input(
        f"  Confirm deletion of '{target['device_name']}' ({item_id})? (yes/no): "
    ).strip().lower()
    if confirm == "yes":
        items.remove(target)
        print(f"  [OK] Item {item_id} deleted successfully.")
    else:
        print("  Deletion cancelled.")


def mark_item_status(items):
    """
    Change the storage status of an item to Recycled or Disposed.

    Args:
        items (list): The current list of e-waste items (modified in place).
    """
    print("\n  ── Mark Item Status ──")
    item_id = input("  Enter Item ID: ").strip().upper()
    target = next((i for i in items if i["id"] == item_id), None)

    if not target:
        print(f"  [ERROR] Item ID '{item_id}' not found.")
        return

    print(f"  Current Status: {target['storage_status']}")
    print("  Available Statuses: Recycled | Disposed")
    new_status = input("  Enter New Status: ").strip().title()

    if new_status not in ["Recycled", "Disposed"]:
        print("  [ERROR] Invalid status. Choose 'Recycled' or 'Disposed'.")
        return

    target["storage_status"] = new_status
    print(f"  [OK] Status of {item_id} updated to '{new_status}'.")


# ─────────────────────────────────────────────
# Search and Sorting
# ─────────────────────────────────────────────

def search_item(items):
    """
    Search for e-waste items by Item ID or Device Name (case-insensitive).

    Args:
        items (list): List of all e-waste items to search through.
    """
    print("\n  ── Search E-Waste Items ──")
    print("  1. Search by Item ID")
    print("  2. Search by Device Name")
    choice = input("  Enter choice: ").strip()

    if choice == "1":
        item_id = input("  Enter Item ID: ").strip().upper()
        results = [i for i in items if i["id"] == item_id]
    elif choice == "2":
        name = input("  Enter Device Name (partial match allowed): ").strip().lower()
        results = [i for i in items if name in i["device_name"].lower()]
    else:
        print("  [ERROR] Invalid choice.")
        return

    if results:
        print(f"\n  Found {len(results)} result(s):")
        display_items(results)
    else:
        print("  No matching items found.")


def sort_items(items):
    """
    Sort and display e-waste items by weight (descending) or category.

    Args:
        items (list): List of e-waste items to sort.
    """
    print("\n  ── Sort E-Waste Items ──")
    print("  1. Sort by Weight (Highest to Lowest)")
    print("  2. Sort by Category")
    choice = input("  Enter choice: ").strip()

    if choice == "1":
        sorted_list = sorted(items, key=lambda x: x["weight"], reverse=True)
        print("\n  Items sorted by Weight (Highest to Lowest):")
    elif choice == "2":
        sorted_list = sorted(items, key=lambda x: x["category"])
        print("\n  Items sorted by Category:")
    else:
        print("  [ERROR] Invalid choice.")
        return

    display_items(sorted_list)


# ─────────────────────────────────────────────
# Billing and Fee Calculation
# ─────────────────────────────────────────────

def calculate_fee(items):
    """
    Calculate recycling fees for a customer submission.

    Applies a 5 % bulk discount when total weight exceeds 50 kg.
    Displays an item-wise breakdown, total weight, any discount, and the
    final payable amount.

    Args:
        items (list): Full item list used to look up selected entries.
    """
    print("\n  ── Billing and Fee Calculation ──")
    print("  Enter Item IDs to include (comma-separated, e.g. EW001,EW002):")
    raw_ids = input("  Item IDs: ").strip().upper().split(",")
    selected_ids = [id_.strip() for id_ in raw_ids]

    selected_items = [i for i in items if i["id"] in selected_ids]
    if not selected_items:
        print("  [ERROR] No valid items found for the entered IDs.")
        return

    print(f"\n  {'─'*70}")
    print(f"  {'Item ID':<10} {'Device Name':<20} {'Weight':>10} {'Fee/kg':>10} {'Subtotal':>12}")
    print(f"  {'─'*70}")

    total_weight = 0.0
    total_fee = 0.0
    for item in selected_items:
        subtotal = item["weight"] * item["fee_per_kg"]
        total_weight += item["weight"]
        total_fee += subtotal
        print(
            f"  {item['id']:<10} {item['device_name']:<20} "
            f"{item['weight']:>10.2f} {item['fee_per_kg']:>10.2f} {subtotal:>12.2f}"
        )

    print(f"  {'─'*70}")
    print(f"  {'Total Weight:':<42} {total_weight:>10.2f} kg")
    print(f"  {'Gross Recycling Fee (LKR):':<42} {total_fee:>12.2f}")

    # Bulk discount
    discount_amount = 0.0
    if total_weight > BULK_DISCOUNT_THRESHOLD:
        discount_amount = total_fee * BULK_DISCOUNT_RATE
        print(f"  {'Bulk Discount (5%):':<42} -{discount_amount:>11.2f}")

    final_amount = total_fee - discount_amount
    print(f"  {'─'*70}")
    print(f"  {'FINAL PAYABLE AMOUNT (LKR):':<42} {final_amount:>12.2f}")
    print(f"  {'─'*70}")


# ─────────────────────────────────────────────
# Storage Capacity Monitoring
# ─────────────────────────────────────────────

def monitor_storage(items):
    """
    Display the current storage utilisation and issue alerts as needed.

    Warns when utilisation exceeds 80 % and reports full capacity.

    Args:
        items (list): List of all e-waste items.
    """
    print("\n  ── Storage Capacity Monitor ──")
    stored_weight = get_total_stored_weight(items)
    utilisation = stored_weight / STORAGE_CAPACITY
    available = STORAGE_CAPACITY - stored_weight

    print(f"\n  Total Storage Capacity : {STORAGE_CAPACITY:.0f} kg")
    print(f"  Currently Stored       : {stored_weight:.2f} kg  ({utilisation*100:.1f}%)")
    print(f"  Available Space        : {available:.2f} kg")

    bar_filled = int(utilisation * 40)
    bar = "[" + "█" * bar_filled + "░" * (40 - bar_filled) + "]"
    print(f"\n  {bar}  {utilisation*100:.1f}%")

    if stored_weight >= STORAGE_CAPACITY:
        print("\n  [CRITICAL] Storage is FULL. No new items can be added.")
    elif utilisation >= STORAGE_WARNING_THRESHOLD:
        print("\n  [WARNING] Storage exceeds 80% capacity. Plan immediate disposal.")
    else:
        print("\n  Storage levels are within acceptable limits.")


# ─────────────────────────────────────────────
# Low Storage / Hazard Alerts
# ─────────────────────────────────────────────

def hazard_alert(items):
    """
    Identify hazardous items stored beyond the 30-day safety threshold
    and categories with the highest accumulation.

    Args:
        items (list): List of all e-waste items.
    """
    print("\n  ── Hazard and Storage Alerts ──")
    today = datetime.today().date()
    overdue_hazards = []

    for item in items:
        if item["category"] == "Hazardous" and item["storage_status"] == "Stored":
            date_added = datetime.strptime(item["date_added"], "%Y-%m-%d").date()
            days_stored = (today - date_added).days
            if days_stored > HAZARD_DAYS_LIMIT:
                overdue_hazards.append((item, days_stored))

    # Hazardous items overdue
    if overdue_hazards:
        print(f"\n  [ALERT] {len(overdue_hazards)} hazardous item(s) stored > {HAZARD_DAYS_LIMIT} days:\n")
        print(f"  {'ID':<8} {'Device Name':<20} {'Days Stored':<14} Action Required")
        print(f"  {'─'*60}")
        for item, days in overdue_hazards:
            print(f"  {item['id']:<8} {item['device_name']:<20} {days:<14} URGENT DISPOSAL")
    else:
        print("\n  No hazardous items require urgent disposal.")

    # Category accumulation analysis
    print("\n  ── Category Accumulation ──")
    category_weight = {}
    for item in items:
        if item["storage_status"] == "Stored":
            cat = item["category"]
            category_weight[cat] = category_weight.get(cat, 0) + item["weight"]

    if category_weight:
        for cat, weight in sorted(category_weight.items(), key=lambda x: x[1], reverse=True):
            bar = "█" * min(int(weight / 2), 30)
            print(f"  {cat:<20} {weight:>8.2f} kg  {bar}")
    else:
        print("  No stored items to analyse.")


# ─────────────────────────────────────────────
# Report Generation
# ─────────────────────────────────────────────

def generate_report(items):
    """
    Generate a summary environmental report saved as a text file.

    The report includes total weight collected, total recycling fees
    earned, item counts by category, and lists of recycled / disposed
    items for the current date.

    Args:
        items (list): List of all e-waste items.
    """
    print("\n  ── Generating Environmental Impact Report ──")
    today_str = datetime.today().strftime("%Y-%m-%d")
    report_filename = f"AEWMS_Report_{today_str}.txt"

    today_items = [i for i in items if i["date_added"] == today_str]
    total_weight_all = sum(i["weight"] for i in items)
    total_weight_today = sum(i["weight"] for i in today_items)
    total_fees = sum(i["weight"] * i["fee_per_kg"] for i in items)
    recycled_count = sum(1 for i in items if i["storage_status"] == "Recycled")
    disposed_count = sum(1 for i in items if i["storage_status"] == "Disposed")
    stored_count   = sum(1 for i in items if i["storage_status"] == "Stored")

    report_lines = [
        "=" * 60,
        "  GREEN LANTERN CORPS RECYCLERS",
        "  Automated E-Waste Management System – Report",
        f"  Generated: {datetime.today().strftime('%Y-%m-%d %H:%M:%S')}",
        "=" * 60,
        "",
        "STORAGE SUMMARY",
        f"  Total Items Recorded   : {len(items)}",
        f"  Items Stored           : {stored_count}",
        f"  Items Recycled         : {recycled_count}",
        f"  Items Disposed         : {disposed_count}",
        "",
        "WEIGHT SUMMARY",
        f"  Total Weight (All)     : {total_weight_all:.2f} kg",
        f"  Weight Added Today     : {total_weight_today:.2f} kg",
        f"  Storage Used           : {get_total_stored_weight(items):.2f} / {STORAGE_CAPACITY} kg",
        "",
        "FINANCIAL SUMMARY",
        f"  Total Recycling Fees   : LKR {total_fees:,.2f}",
        "",
        "CATEGORY BREAKDOWN",
    ]
    category_counts = {}
    for item in items:
        cat = item["category"]
        category_counts[cat] = category_counts.get(cat, 0) + 1
    for cat, count in category_counts.items():
        report_lines.append(f"  {cat:<22}: {count} item(s)")

    report_lines += [
        "",
        "ITEMS ADDED TODAY",
    ]
    if today_items:
        for item in today_items:
            report_lines.append(
                f"  [{item['id']}] {item['device_name']} – "
                f"{item['weight']} kg – {item['category']}"
            )
    else:
        report_lines.append("  No new items recorded today.")

    report_lines += ["", "=" * 60, "  END OF REPORT", "=" * 60]

    report_text = "\n".join(report_lines)
    with open(report_filename, "w") as report_file:
        report_file.write(report_text)

    print(f"\n  [OK] Report saved to '{report_filename}'.")
    print(report_text)


# ─────────────────────────────────────────────
# Main Menu
# ─────────────────────────────────────────────

def display_menu():
    """Display the main navigation menu."""
    print("\n" + "=" * 55)
    print("   GREEN LANTERN CORPS – E-WASTE MANAGEMENT SYSTEM")
    print("=" * 55)
    print("   1.  Display All E-Waste Items")
    print("   2.  Add New E-Waste Item")
    print("   3.  Update Item Weight")
    print("   4.  Delete E-Waste Item")
    print("   5.  Mark Item as Recycled / Disposed")
    print("   6.  Search E-Waste Items")
    print("   7.  Sort E-Waste Items")
    print("   8.  Billing and Fee Calculation")
    print("   9.  Storage Capacity Monitor")
    print("  10.  Hazard and Accumulation Alerts")
    print("  11.  Generate Environmental Report")
    print("   0.  Save and Exit")
    print("=" * 55)


def main():
    """
    Entry point – loads data, runs the menu loop, saves on exit.

    Handles invalid menu input gracefully without crashing.
    """
    items = load_data()
    print("\n  Welcome to the Green Lantern Corps AEWMS.")
    print(f"  {len(items)} record(s) loaded.")

    while True:
        display_menu()
        choice = input("\n  Enter your choice: ").strip()

        if choice == "1":
            display_items(items)
        elif choice == "2":
            add_item(items)
        elif choice == "3":
            update_item(items)
        elif choice == "4":
            delete_item(items)
        elif choice == "5":
            mark_item_status(items)
        elif choice == "6":
            search_item(items)
        elif choice == "7":
            sort_items(items)
        elif choice == "8":
            calculate_fee(items)
        elif choice == "9":
            monitor_storage(items)
        elif choice == "10":
            hazard_alert(items)
        elif choice == "11":
            generate_report(items)
        elif choice == "0":
            save_data(items)
            print("\n  Thank you for using AEWMS. Goodbye!\n")
            break
        else:
            print("\n  [ERROR] Invalid choice. Please enter a number from 0 to 11.")


# ─────────────────────────────────────────────
# Program Entry
# ─────────────────────────────────────────────
if __name__ == "__main__":
    main()
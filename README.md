# Green Lantern Corps Recyclers: Automated E-Waste Management System (AEWMS)



- **Version:** 1.0
- **Language:** Python 3 (standard library only, no external dependencies)

---

## Features

| # | Feature | Description |
|---|---------|-------------|
| 1 | Display items | Shows all records in a formatted table |
| 2 | Add item | Adds a new item with input validation and a storage capacity check |
| 3 | Update weight | Changes the weight of an existing item by ID |
| 4 | Delete item | Removes an item after a yes/no confirmation |
| 5 | Mark status | Sets an item's status to `Recycled` or `Disposed` |
| 6 | Search | Finds items by ID (exact) or device name (partial, case-insensitive) |
| 7 | Sort | Sorts by weight (highest to lowest) or by category |
| 8 | Billing | Calculates recycling fees for selected items, with a bulk discount |
| 9 | Storage monitor | Shows utilisation with a progress bar and warning alerts |
| 10 | Hazard alerts | Flags hazardous items stored too long and shows weight per category |
| 11 | Report | Writes a summary report to a dated `.txt` file |
| 0 | Save and exit | Saves all data to JSON and quits |

---

## Requirements

- Python 3.6 or later
- No `pip install` needed. The program uses only `json`, `os`, and `datetime` from the standard library.

---

## How to Run

1. Save the program file (for example, as `aewms.py`).
2. Open a terminal in the same folder.
3. Run:

```bash
python aewms.py
```

On some systems you may need `python3 aewms.py`.

On first launch, no data file exists, so the program loads **5 sample records** so you can try it right away. Choose option `0` to save your data and exit. On the next launch, your saved data is loaded instead.

---

## Data Model

Each e-waste item is stored as a dictionary:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Auto-generated, format `EW001`, `EW002`, … |
| `device_name` | string | Name of the device (e.g. Laptop) |
| `category` | string | `Recyclable`, `Hazardous`, or `Non-Recyclable` |
| `weight` | float | Weight in kg (must be > 0) |
| `fee_per_kg` | float | Recycling fee per kg in LKR (must be ≥ 0) |
| `storage_status` | string | `Stored`, `Recycled`, or `Disposed` |
| `date_added` | string | Date in `YYYY-MM-DD` format |

---

## Business Rules (Configurable Constants)

These are defined at the top of the file and can be changed there.

| Constant | Default | Meaning |
|----------|---------|---------|
| `DATA_FILE` | `ewaste_data.json` | File used for saving and loading records |
| `STORAGE_CAPACITY` | `1000` | Maximum storage in kg |
| `STORAGE_WARNING_THRESHOLD` | `0.80` | Utilisation (80%) at which a warning is shown |
| `BULK_DISCOUNT_THRESHOLD` | `50` | Total weight (kg) above which a discount applies |
| `BULK_DISCOUNT_RATE` | `0.05` | 5% bulk discount |
| `HAZARD_DAYS_LIMIT` | `30` | Days a hazardous item may be stored before an alert |

**Notes on how the rules work:**

- Only items with status `Stored` count toward storage usage.
- Items cannot be added once storage is full, or if the new item would exceed the remaining capacity.
- The bulk discount applies to the combined weight of the items selected in the billing screen.
- Hazard alerts apply only to `Hazardous` items that are still `Stored`.

---

## Usage Guide

### Main menu

```
=======================================================
   GREEN LANTERN CORPS – E-WASTE MANAGEMENT SYSTEM
=======================================================
   1.  Display All E-Waste Items
   2.  Add New E-Waste Item
   ...
  11.  Generate Environmental Report
   0.  Save and Exit
=======================================================
```

Type a number and press Enter. Invalid input shows an error and returns to the menu.

### Adding an item (option 2)

You will be prompted for:

1. Device name (cannot be empty)
2. Category (`Recyclable`, `Hazardous`, or `Non-Recyclable`; case-insensitive)
3. Weight in kg
4. Recycling fee per kg in LKR

### Billing (option 8)

Enter item IDs separated by commas, for example:

```
EW001,EW002
```

The program prints an item-wise breakdown, total weight, gross fee, any bulk discount, and the final payable amount in LKR.

### Reports (option 11)

Creates a file named `AEWMS_Report_YYYY-MM-DD.txt` in the current folder. It contains item counts by status, weight and fee totals, a category breakdown, and items added today. The report is also printed to the screen.

---

## Files Created by the Program

| File | Created when | Purpose |
|------|--------------|---------|
| `ewaste_data.json` | You choose `0` (Save and Exit) | Stores all item records |
| `AEWMS_Report_<date>.txt` | You choose `11` | Daily summary report |

> **Important:** Changes are only written to disk when you exit with option `0`. Closing the terminal or pressing Ctrl+C will lose unsaved changes.

---

## Project Structure

```
aewms.py
├── Constants               Configurable settings
├── Data Persistence        load_data(), save_data()
├── Display                 display_items()
├── Collection Management   generate_id(), get_total_stored_weight(),
│                           add_item(), update_item(), delete_item(),
│                           mark_item_status()
├── Search and Sorting      search_item(), sort_items()
├── Billing                 calculate_fee()
├── Storage Monitoring      monitor_storage()
├── Alerts                  hazard_alert()
├── Reporting               generate_report()
└── Main Menu               display_menu(), main()
```

---

## Known Limitations

- **Update weight does not re-check capacity.** Raising an item's weight can push stored weight above 1000 kg.
- **No Ctrl+C handling.** Interrupting the program skips saving.
- **Corrupted JSON is not handled.** If `ewaste_data.json` is edited by hand and becomes invalid, the program will raise an error on startup.
- **Report totals include all items.** "Total Weight" and "Total Recycling Fees" cover every record regardless of status, not only items collected today.
- **Sort is display-only.** Sorting does not change the stored order of records.

---

## Possible Future Improvements

- Auto-save after every change
- Input validation loops that re-prompt instead of returning to the menu
- Export billing receipts to a file
- Unit tests for the fee and storage calculations
- Date-range filtering for reports

---

## Author
---abdullah--

Student, CSE4202 – Fundamentals in Programming

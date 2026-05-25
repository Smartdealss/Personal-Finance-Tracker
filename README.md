# 💰 Personal Finance Tracker

A simple command-line (CLI) application for personal finance management, written in Python. Track your income and expenses with ease — all data is stored in a CSV file, no external libraries required.

---

## Features

- ➕ **Add income** – enter amount, description, and category
- ➖ **Add expense** – amount, description, category (e.g. food, transport)
- 📊 **Financial report** – full transaction table with a summary
- 💾 **CSV storage** – data saved to `finances.csv`, viewable in any spreadsheet app

---

## Getting Started

**Requirements:** Python 3.x (standard library only, no extra packages)

```bash
python tracker.py
```

### Adding income

```
Amount (€): 1200
Description: Monthly salary
Category: salary
✓ Added: +1200.00 € (Monthly salary)
```

### Adding an expense

```
Amount (€): 45.50
Description: Weekly groceries
Category: food
✓ Recorded: -45.50 € (Weekly groceries, food)
```

### Financial report

```
Type         Amount   Description               Category        Date
---------------------------------------------------------------------------
income      +1200.00  Monthly salary            salary          2025-05-20
expense       -45.50  Weekly groceries          food            2025-05-21
---------------------------------------------------------------------------
Total income:                  +1200.00 €
Total expenses:                  -45.50 €
Balance:                       +1154.50 €
```

---

## Data structure

Data is saved to `finances.csv` in the following format:

| type    | amount | description      | category | date       |
|---------|--------|------------------|----------|------------|
| income  | 1200.0 | Monthly salary   | salary   | 2025-05-20 |
| expense | 45.50  | Weekly groceries | food     | 2025-05-21 |

---

## Project structure

```
finance-tracker/
├── tracker.py      # Main program
├── finances.csv    # Data file (created automatically)
└── README.md
```

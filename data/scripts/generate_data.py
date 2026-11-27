"""Generate reproducible FinPilot fixtures using only the standard library."""
import argparse
import calendar
import csv
import random
from datetime import date
from pathlib import Path

DATA = Path(__file__).resolve().parents[1]
SCHEMA = {
    "users": "user_id age_group occupation_group monthly_income",
    "budgets": "budget_id user_id month budget_amount",
    "transactions": "transaction_id user_id transaction_date amount category transaction_type is_essential related_transaction_id",
    "preferences": "user_id protected_categories",
}
CATEGORIES = ("food", "housing", "transport", "shopping", "entertainment", "health", "other", "travel")
# Survey Q3, excluding two non-responses. Upper bound for the open band is assumed.
INCOME_BANDS = [(3, 4), (5, 9), (10, 14), (15, 19), (20, 25)]
INCOME_WEIGHTS = [5, 3, 4, 4, 3]
DELIVERY_BANDS = [(0, 0), (1, 2), (3, 5), (6, 7)]
DELIVERY_WEIGHTS = [4, 4, 11, 2]
DRINK_BANDS = [(1, 2), (3, 5), (6, 7), (8, 10)]
DRINK_WEIGHTS = [10, 6, 4, 1]


def generate(user_count, start, months, seed, output):
    rng = random.Random(seed)
    tables = {name: [] for name in SCHEMA}
    for index in range(1, user_count + 1):
        user = f"U{index:03}"
        age = rng.choices(["under20", "20-24", "25-30", "over30"], [1, 13, 6, 1])[0]
        occupation = rng.choices(["office", "student", "freelance"], [9, 8, 4])[0]
        low, high = rng.choices(INCOME_BANDS, INCOME_WEIGHTS)[0]
        income = rng.randint(low, high) * 1_000_000
        delivery = rng.randint(*rng.choices(DELIVERY_BANDS, DELIVERY_WEIGHTS)[0])
        drinks = rng.randint(*rng.choices(DRINK_BANDS, DRINK_WEIGHTS)[0])
        tables["users"].append((user, age, occupation, income))
        tables["preferences"].append((user, "housing|health"))
        for offset in range(months):
            year, month_index = divmod(start.year * 12 + start.month - 1 + offset, 12)
            month = month_index + 1
            period = f"{year:04}-{month:02}"
            days = calendar.monthrange(year, month)[1]
            budget = income * rng.randint(65, 90) // 100
            tables["budgets"].append((f"{user}-{period}", user, period, budget))
            # Recurring essentials plus variable purchases and occasional discretionary spikes.
            purchases = [(1, "housing", True, income // 4)]
            purchases.extend((day, "food", True, rng.randrange(25, 65) * 1000) for day in range(1, days + 1))
            purchases.extend((day, "transport", True, rng.randrange(40, 100) * 1000) for day in range(3, days + 1, 4))
            for weekly_count, low, high in ((delivery, 55, 120), (drinks, 25, 65)):
                purchases.extend((rng.randint(1, days), "food", False, rng.randrange(low, high) * 1000)
                                 for _ in range(round(weekly_count * days / 7)))
            purchases.extend((rng.randint(1, days), category, False, rng.randrange(80, 550) * 1000)
                             for category in ("shopping", "entertainment", "other"))
            if rng.random() < 0.30:
                purchases.append((rng.randint(1, days), "shopping", False, rng.randrange(5, 18) * 100_000))
            for day, category, essential, amount in sorted(purchases):
                transaction_id = f"T{len(tables['transactions']) + 1:06}"
                tables["transactions"].append((transaction_id, user, date(year, month, day).isoformat(),
                                               amount, category, "expense", str(essential).lower(), ""))
    output.mkdir(parents=True, exist_ok=True)
    for name, fields in SCHEMA.items():
        with (output / f"{name}.csv").open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(fields.split())
            writer.writerows(tables[name])
        print(f"{name}: {len(tables[name])}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--users", type=int, default=30)
    parser.add_argument("--start", default="2026-09", help="First month (YYYY-MM)")
    parser.add_argument("--months", type=int, default=3)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=Path, default=DATA / "synthetic")
    args = parser.parse_args()
    try:
        start = date.fromisoformat(args.start + "-01")
    except ValueError:
        parser.error("--start must be YYYY-MM")
    if args.users < 1 or args.months < 1 or start.year * 12 + start.month - 1 + args.months > 120000:
        parser.error("use positive counts and a date range within year 9999")
    generate(args.users, start, args.months, args.seed, args.output)

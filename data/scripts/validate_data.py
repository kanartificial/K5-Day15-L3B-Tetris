"""Validate CSV integrity and reconcile the expected results of synthetic fixtures."""
import argparse
import calendar
import csv
import json
from collections import Counter
from datetime import date
from pathlib import Path

from generate_data import CATEGORIES, DATA, SCHEMA


def positive_int(value):
    return int(value) > 0 and str(int(value)) == value


def iso_date(value):
    parsed = date.fromisoformat(value)
    if parsed.isoformat() != value:
        raise ValueError("expected YYYY-MM-DD")
    return parsed


def validate_tables(directory, start, end):
    errors, tables = [], {}
    for table, fields in SCHEMA.items():
        with (directory / f"{table}.csv").open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames != fields.split():
                raise ValueError(f"{table}: invalid header")
            rows = list(reader)
        keys = Counter(row[reader.fieldnames[0]] for row in rows)
        for line, row in enumerate(rows, 2):
            for field in fields.split():
                if row[field] in (None, "") and field != "related_transaction_id":
                    errors.append(f"{table}:{line}: missing {field}")
            if None in row or None in row.values():
                errors.append(f"{table}:{line}: invalid column count")
            if keys[row[reader.fieldnames[0]]] > 1:
                errors.append(f"{table}:{line}: duplicate key")
        tables[table] = rows

    users = {row["user_id"] for row in tables["users"]}
    budgets = Counter((row["user_id"], row["month"]) for row in tables["budgets"])
    preferences = {row["user_id"] for row in tables["preferences"]}
    transactions = {row["transaction_id"]: row for row in tables["transactions"]}
    refunds = Counter()
    if not users or preferences != users:
        errors.append("preferences must cover all users exactly once")
    if not tables["transactions"]:
        errors.append("transactions must be nonempty")
    if not budgets or {user for user, month in budgets} != users:
        errors.append("every user must have a budget")
    for table, rows in tables.items():
        for line, row in enumerate(rows, 2):
            try:
                user = row["user_id"]
                valid = user in users
                if table == "users":
                    valid &= positive_int(row["monthly_income"])
                    valid &= row["age_group"] in {"under20", "20-24", "25-30", "over30"}
                    valid &= row["occupation_group"] in {"office", "student", "freelance"}
                elif table == "preferences":
                    categories = row["protected_categories"].split("|")
                    valid &= set(categories) <= set(CATEGORIES) and len(categories) == len(set(categories))
                elif table == "budgets":
                    month = row["month"]
                    iso_date(month + "-01")
                    valid &= start <= month <= end and budgets[user, month] == 1
                    valid &= positive_int(row["budget_amount"])
                else:
                    day = iso_date(row["transaction_date"]).isoformat()
                    kind = row["transaction_type"]
                    valid &= start <= day[:7] <= end and budgets[user, day[:7]] == 1
                    valid &= positive_int(row["amount"]) and row["category"] in CATEGORIES
                    valid &= kind in {"expense", "refund", "transfer"}
                    valid &= row["is_essential"] in {"true", "false"}
                    ref = row["related_transaction_id"]
                    if kind == "refund":
                        original = transactions[ref]
                        if original["transaction_date"][:7] != day[:7]:
                            errors.append(f"{table}:{line}: cross-period refund pending policy")
                            continue
                        refunds[ref] += int(row["amount"])
                        valid &= original["user_id"] == user and original["transaction_type"] == "expense"
                        valid &= original["transaction_date"] <= day
                        valid &= original["category"] == row["category"]
                        valid &= original["is_essential"] == row["is_essential"]
                    else:
                        valid &= ref == ""
                if not valid:
                    errors.append(f"{table}:{line}: invalid value or relationship")
            except (ValueError, TypeError, KeyError, AttributeError):
                errors.append(f"{table}:{line}: invalid type or reference")
    for ref, total in refunds.items():
        try:
            if total > int(transactions[ref]["amount"]):
                errors.append(f"{ref}: refunds exceed original amount")
        except (ValueError, TypeError):
            errors.append(f"{ref}: invalid original amount")
    return tables, errors


def fixture_result(status, spent=None, forecast=None, gap=None, candidate_limits=None,
                   forbidden_ids=(), max_saving=0, selected_saving=0):
    limits = candidate_limits or {}
    return dict(status=status, spent=spent, forecast=forecast, gap=gap,
                allowed_candidate_ids=sorted(limits), forbidden_candidate_ids=sorted(forbidden_ids),
                candidate_cap_total=sum(limits.values()), max_saving=max_saving,
                selected_saving=selected_saving,
                remaining_gap=None if gap is None else max(0, gap - selected_saving))


def validated_saving(selection, limits, budget_cap):
    """Validate the entire proposed selection before crediting any savings."""
    if len(selection) > 3:
        return None
    used = set()
    total = 0
    for item in selection:
        candidate_id, amount = item["candidate_id"], item["saving_amount"]
        if (candidate_id in used or candidate_id not in limits or type(amount) is not int
                or not 0 < amount <= limits[candidate_id]):
            return None
        used.add(candidate_id)
        total += amount
    return total if total <= budget_cap else None


def reconcile(sample):
    """Reference arithmetic for the test fixtures only."""
    month, budget = sample["month"], sample["budget_amount"]
    cutoff = iso_date(sample["as_of"])
    if cutoff.isoformat()[:7] != month:
        raise ValueError("as_of must fall within month")
    if budget <= 0:
        return fixture_result("invalid_budget")
    protected = set(sample["protected_categories"])
    eligible = {}
    for row in sample["transactions"]:
        day = iso_date(row["transaction_date"])
        known_on = iso_date(row.get("known_on", row["transaction_date"]))
        if max(day, known_on) <= cutoff and day.isoformat()[:7] == month:
            eligible.setdefault(row["transaction_id"], row)
    spent = flexible = 0
    for row in eligible.values():
        kind = row["transaction_type"]
        if kind == "transfer":
            continue
        original = eligible.get(row["related_transaction_id"]) if kind == "refund" else row
        if original is None:
            return fixture_result("refund_reference_outside_snapshot")
        amount = -row["amount"] if kind == "refund" else row["amount"]
        spent += amount
        if not original["is_essential"] and original["category"] not in protected:
            flexible += amount
    days_left = calendar.monthrange(cutoff.year, cutoff.month)[1] - cutoff.day
    coverage = sample["coverage_days"]
    if not 0 <= coverage <= cutoff.day:
        raise ValueError("invalid coverage_days")
    planned = [p for p in sample["planned_expenses"]
               if iso_date(p["known_on"]) <= cutoff < iso_date(p["due_on"])
               and p["due_on"][:7] == month]
    if len({p["id"] for p in planned}) != len(planned):
        raise ValueError("duplicate planned expense ID")
    forbidden = {p["id"] for p in planned if p["is_essential"] or p["category"] in protected}
    essential = sum(p["amount"] for p in planned if p["id"] in forbidden)
    flexible_projection = round(flexible * days_left / coverage) if coverage >= 7 else 0
    forecast = spent + essential + flexible_projection if coverage >= 7 else None
    if spent > budget:
        status = "actual_over"
    elif forecast is None:
        status = "insufficient_data"
    elif forecast > budget:
        status = "forecast_over"
    else:
        status = "safe"
    gap = max(0, max(spent, forecast if forecast is not None else spent) - budget)
    if status == "insufficient_data":
        gap = None
    limits = {p["id"]: p["amount"] for p in planned
              if p["id"] not in forbidden and gap and flexible_projection > 0}
    max_saving = min(max(0, flexible_projection), sum(limits.values()))
    savings = validated_saving(sample.get("recommendations", []), limits, max_saving)
    if savings is None:
        status, savings = "invalid_selection", 0
    return fixture_result(status, spent, forecast, gap, limits, forbidden, max_saving, savings)


def validate_cases():
    all_cases = []
    errors = []
    for filename in ("demo_cases.json", "edge_cases.json"):
        cases = json.loads((DATA / "demo" / filename).read_text(encoding="utf-8"))
        all_cases.extend(cases)
        for case in cases:
            actual = reconcile(case["input"])
            if actual != case["expected_output"] or case["source_type"] != "synthetic":
                errors.append(f"{case['case_id']}: expected output mismatch: {actual}")
    if Counter(case["case_id"] for case in all_cases) != Counter(f"TC{i:02}" for i in range(1, 20)):
        errors.append("expected each of TC01–TC19 exactly once")
    return len(all_cases), errors


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DATA / "synthetic")
    parser.add_argument("--start", default="2026-09")
    parser.add_argument("--end", default="2026-11")
    args = parser.parse_args()
    iso_date(args.start + "-01")
    iso_date(args.end + "-01")
    if args.start > args.end:
        parser.error("--start must not be later than --end")
    tables, errors = validate_tables(args.input, args.start, args.end)
    case_count, case_errors = validate_cases()
    for table, rows in tables.items():
        print(f"{table}: {len(rows)}")
    days = [row["transaction_date"] or "" for row in tables["transactions"]]
    if days:
        print(f"transaction dates: {min(days)} to {max(days)}")
    print(f"CSV violations: {len(errors)}")
    print(f"cases: {case_count}; case violations: {len(case_errors)}")
    for error in errors + case_errors:
        print(error)
    print("FAIL" if errors or case_errors else "PASS")
    raise SystemExit(int(bool(errors or case_errors)))

"""Công cụ của bài toán — NHÓM VIẾT. Khớp spec.md §4 và data/DATA_CONTRACT.md.

Mỗi công cụ là một hàm Python có @tool với docstring 4 ý:
    tên · input · output · có tác động ra ngoài không.
Chỉ dùng thư viện chuẩn Python 3.10+.
"""
import calendar
import csv
import datetime
import json
import os
import re
from collections import defaultdict

from tracing import tool, TOOLS  # noqa: F401

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data")
SYNTH_DIR = os.path.join(DATA_DIR, "synthetic")
DEMO_DIR = os.path.join(DATA_DIR, "demo")

CATEGORY_VI = {
    "food": "Ăn uống",
    "shopping": "Mua sắm",
    "entertainment": "Giải trí",
    "transport": "Đi lại",
    "travel": "Du lịch",
    "housing": "Nhà ở",
    "health": "Y tế",
    "other": "Khác",
}

# Trọng số độ khó cắt (cao hơn = khó cắt hơn; protected/essential coi như vô cùng)
DISUTILITY_WEIGHTS = {
    "entertainment": 1.0,
    "shopping": 1.2,
    "travel": 1.4,
    "food": 1.6,
    "other": 1.5,
    "transport": 2.2,
}


def _iso_date(value: str) -> datetime.date:
    return datetime.date.fromisoformat(value.strip())


def _load_demo_case(case_id: str) -> dict | None:
    target = case_id.strip().upper()
    for fname in ("demo_cases.json", "edge_cases.json"):
        path = os.path.join(DEMO_DIR, fname)
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as f:
            for item in json.load(f):
                if item.get("case_id", "").upper() == target:
                    return item
    return None


def _load_synthetic_snapshot(user_id: str, month: str, as_of: str) -> dict:
    uid = user_id.strip().upper()
    budget_amount = 0
    with open(os.path.join(SYNTH_DIR, "budgets.csv"), encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            if row["user_id"] == uid and row["month"] == month:
                budget_amount = int(row["budget_amount"])
                break

    protected = []
    prefs_path = os.path.join(SYNTH_DIR, "preferences.csv")
    if os.path.exists(prefs_path):
        with open(prefs_path, encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                if row["user_id"] == uid:
                    protected = [c for c in row["protected_categories"].split("|") if c]
                    break

    txs = []
    with open(os.path.join(SYNTH_DIR, "transactions.csv"), encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            if row["user_id"] == uid and row["transaction_date"][:7] == month:
                txs.append({
                    "transaction_id": row["transaction_id"],
                    "transaction_date": row["transaction_date"],
                    "amount": int(row["amount"]),
                    "category": row["category"],
                    "is_essential": row["is_essential"].lower() == "true",
                    "transaction_type": row["transaction_type"],
                    "related_transaction_id": row["related_transaction_id"] or None,
                })

    cutoff = _iso_date(as_of)
    return {
        "month": month,
        "as_of": as_of,
        "budget_amount": budget_amount,
        "coverage_days": cutoff.day,
        "protected_categories": protected,
        "transactions": txs,
        "planned_expenses": [],
    }


def _quantile(sorted_vals: list[float], q: float) -> float:
    if not sorted_vals:
        return 0.0
    if len(sorted_vals) == 1:
        return float(sorted_vals[0])
    pos = q * (len(sorted_vals) - 1)
    lo = int(pos)
    hi = min(lo + 1, len(sorted_vals) - 1)
    frac = pos - lo
    return sorted_vals[lo] * (1.0 - frac) + sorted_vals[hi] * frac


def _iqr_filtered_daily(daily_values: list[int]) -> list[int]:
    if len(daily_values) < 4:
        return daily_values
    s = sorted(daily_values)
    q1, q3 = _quantile(s, 0.25), _quantile(s, 0.75)
    upper = q3 + 1.5 * (q3 - q1)
    filtered = [v for v in daily_values if v <= upper]
    return filtered or daily_values


def _compute_p50_p85(daily_flex: dict[str, int], coverage: int, days_left: int,
                     base_spent_and_essential: int, point_projection: int) -> tuple[int, int]:
    if coverage < 7 or days_left <= 0:
        return point_projection, point_projection
    series = sorted(daily_flex.values()) + [0] * max(0, coverage - len(daily_flex))
    cleaned = sorted(_iqr_filtered_daily(series))
    p50_daily = _quantile(cleaned, 0.50)
    p85_daily = _quantile(cleaned, 0.85)
    # Neo P50 quanh dự báo điểm, P85 phản ánh rủi ro đuôi phải theo từng ngày còn lại
    p50 = max(point_projection, base_spent_and_essential + round(p50_daily * days_left))
    p85 = max(p50, base_spent_and_essential + round(p85_daily * days_left))
    return p50, p85


@tool
def get_cashflow_forecast(
    user_id: str = "U010",
    month: str = "2026-11",
    as_of: str = "2026-11-20",
    case_id: str = "",
    payload_json: str = "",
) -> dict:
    """get_cashflow_forecast · Input: user_id/month/as_of hoặc case_id (TC01-TC19) hoặc payload_json ·
    Output: dict gồm status, spent, forecast, forecast_p50, forecast_p85, gap, safe_to_spend_daily,
    data_completeness_score, category_breakdown, allowed_candidates, forbidden_categories ·
    Không tác động ra ngoài."""
    if payload_json.strip():
        sample = json.loads(payload_json)
        source_label = "payload"
    elif case_id.strip():
        loaded = _load_demo_case(case_id)
        if not loaded:
            return {"status": "not_found", "error": f"Không tìm thấy ca {case_id}"}
        sample = loaded["input"]
        source_label = loaded["case_id"]
    else:
        sample = _load_synthetic_snapshot(user_id, month, as_of)
        source_label = f"synthetic:{month}"

    budget = int(sample.get("budget_amount", 0))
    if budget <= 0:
        return {"source": source_label, "status": "invalid_budget", "budget_amount": budget,
                "spent": None, "forecast": None, "gap": None, "safe_to_spend_daily": 0}

    cur_month = sample["month"]
    cutoff = _iso_date(sample["as_of"])
    protected = set(sample.get("protected_categories", []))

    eligible = {}
    for row in sample.get("transactions", []):
        day = _iso_date(row["transaction_date"])
        known_on = _iso_date(row.get("known_on") or row["transaction_date"])
        if max(day, known_on) <= cutoff and day.isoformat()[:7] == cur_month:
            eligible.setdefault(row["transaction_id"], row)

    spent = flexible_spent = essential_spent = 0
    flex_by_cat: dict[str, int] = defaultdict(int)
    essential_by_cat: dict[str, int] = defaultdict(int)
    daily_flex: dict[str, int] = defaultdict(int)
    tx_dates = []

    for row in eligible.values():
        kind = row["transaction_type"]
        if kind == "transfer":
            continue
        original = eligible.get(row.get("related_transaction_id")) if kind == "refund" else row
        if original is None:
            return {"source": source_label, "status": "refund_reference_outside_snapshot",
                    "budget_amount": budget, "spent": None, "forecast": None, "gap": None}
        amt = -int(row["amount"]) if kind == "refund" else int(row["amount"])
        spent += amt
        tx_dates.append(_iso_date(row["transaction_date"]))
        cat = original["category"]
        if original["is_essential"] or cat in protected:
            essential_spent += amt
            essential_by_cat[cat] += amt
        else:
            flexible_spent += amt
            flex_by_cat[cat] += amt
            daily_flex[row["transaction_date"]] += amt

    days_in_month = calendar.monthrange(cutoff.year, cutoff.month)[1]
    days_left = max(0, days_in_month - cutoff.day)
    coverage = int(sample.get("coverage_days", cutoff.day))

    planned = [
        p for p in sample.get("planned_expenses", [])
        if _iso_date(p["known_on"]) <= cutoff < _iso_date(p["due_on"])
        and p["due_on"][:7] == cur_month
    ]
    forbidden_ids = sorted(p["id"] for p in planned if p["is_essential"] or p["category"] in protected)
    planned_essential = sum(int(p["amount"]) for p in planned if p["id"] in forbidden_ids)
    planned_flex = [
        {"id": p["id"], "category": p["category"], "max_saving": int(p["amount"])}
        for p in planned if p["id"] not in forbidden_ids
    ]

    flex_proj = round(flexible_spent * days_left / coverage) if coverage >= 7 else 0
    forecast = spent + planned_essential + flex_proj if coverage >= 7 else None

    if spent > budget:
        status = "actual_over"
    elif forecast is None:
        status = "insufficient_data"
    elif forecast > budget:
        status = "forecast_over"
    else:
        status = "safe"

    gap = None if status == "insufficient_data" else max(0, max(spent, forecast or spent) - budget)
    p50, p85 = _compute_p50_p85(
        daily_flex, coverage, days_left, spent + planned_essential, forecast or spent
    )
    remaining_budget = max(0, budget - spent - planned_essential)
    safe_daily = remaining_budget // max(1, days_left) if days_left > 0 else remaining_budget

    gap_days = (cutoff - max(tx_dates)).days if tx_dates else coverage
    completeness = 0.0 if coverage < 7 else max(0.2, round(1.0 - max(0, gap_days - 1) * 0.2, 2))
    if gap_days > 2 and p85 >= p50:
        p85 = round(p85 * 1.1)

    return {
        "source": source_label,
        "month": cur_month,
        "as_of": sample["as_of"],
        "days_left": days_left,
        "coverage_days": coverage,
        "budget_amount": budget,
        "status": status,
        "spent": spent,
        "essential_spent": essential_spent,
        "flexible_spent": flexible_spent,
        "planned_essential": planned_essential,
        "flexible_projection": flex_proj,
        "forecast": forecast,
        "forecast_p50": p50 if forecast is not None else None,
        "forecast_p85": p85 if forecast is not None else None,
        "gap": gap,
        "safe_to_spend_daily": safe_daily,
        "data_completeness_score": completeness,
        "days_since_last_tx": gap_days,
        "protected_categories": sorted(protected),
        "flexible_by_category": {k: v for k, v in sorted(flex_by_cat.items(), key=lambda x: -x[1]) if v > 0},
        "essential_by_category": {k: v for k, v in sorted(essential_by_cat.items(), key=lambda x: -x[1]) if v > 0},
        "planned_flex_candidates": planned_flex,
        "forbidden_candidate_ids": forbidden_ids,
    }


@tool
def optimize_budget_reduction(forecast_data: dict, target_saving: int = 0) -> dict:
    """optimize_budget_reduction · Input: output từ get_cashflow_forecast và target_saving (VND) ·
    Output: dict phương án cắt giảm tối ưu (khóa danh mục thiết yếu/bảo vệ, ẩn danh PII) ·
    Không tác động ra ngoài."""
    status = forecast_data.get("status")
    if status in ("invalid_budget", "refund_reference_outside_snapshot", "insufficient_data", "not_found"):
        return {
            "status": status,
            "target_saving": 0,
            "max_saving": 0,
            "recommendations": [],
            "remaining_gap": forecast_data.get("gap"),
            "note": "Chưa đủ dữ liệu hợp lệ để tối ưu cắt giảm.",
        }

    gap = int(forecast_data.get("gap") or 0)
    goal = int(target_saving) if target_saving > 0 else gap
    planned_candidates = forecast_data.get("planned_flex_candidates") or []
    flex_proj = int(forecast_data.get("flexible_projection") or 0)

    if goal <= 0:
        return {
            "status": status,
            "target_saving": 0,
            "max_saving": 0,
            "recommendations": [],
            "remaining_gap": 0,
            "locked_categories": forecast_data.get("protected_categories", []),
        }

    # Nhánh 1: Có planned_expenses linh hoạt theo BR06 (tối đa 3 khoản, trong trần)
    if planned_candidates:
        cap_total = sum(c["max_saving"] for c in planned_candidates)
        max_saving = min(max(0, flex_proj), cap_total)
        remaining = min(goal, max_saving)
        recs = []
        for cand in sorted(planned_candidates, key=lambda c: DISUTILITY_WEIGHTS.get(c["category"], 1.5))[:3]:
            if remaining <= 0:
                break
            take = min(cand["max_saving"], remaining)
            if take > 0:
                recs.append({
                    "candidate_id": cand["id"],
                    "category": cand["category"],
                    "category_vi": CATEGORY_VI.get(cand["category"], cand["category"]),
                    "saving_amount": take,
                    "cap": cand["max_saving"],
                })
                remaining -= take
        selected = sum(r["saving_amount"] for r in recs)
        return {
            "status": status,
            "target_saving": goal,
            "max_saving": max_saving,
            "selected_saving": selected,
            "remaining_gap": max(0, gap - selected),
            "recommendations": recs,
            "forbidden_candidate_ids": forecast_data.get("forbidden_candidate_ids", []),
            "locked_categories": forecast_data.get("protected_categories", []),
        }

    # Nhánh 2: Tối ưu bậc hai có trọng số trên các danh mục linh hoạt (theo ngày còn lại)
    flex_by_cat = forecast_data.get("flexible_by_category") or {}
    days_left = max(1, int(forecast_data.get("days_left") or 1))
    coverage = max(1, int(forecast_data.get("coverage_days") or 1))
    caps = {}
    for cat, spent_cat in flex_by_cat.items():
        projected_cat = round(spent_cat * days_left / coverage)
        if projected_cat > 0:
            caps[cat] = projected_cat

    if not caps:
        return {
            "status": status,
            "target_saving": goal,
            "max_saving": 0,
            "selected_saving": 0,
            "remaining_gap": gap,
            "recommendations": [],
            "locked_categories": forecast_data.get("protected_categories", []),
        }

    # Nghiệm đóng tỉ lệ theo x_i^2 / w_i, giới hạn theo trần từng danh mục
    max_saving = sum(caps.values())
    needed = min(goal, max_saving)
    scores = {cat: (cap * cap) / DISUTILITY_WEIGHTS.get(cat, 1.5) for cat, cap in caps.items()}
    total_score = sum(scores.values()) or 1.0

    alloc = {}
    rem = needed
    ordered = sorted(caps.keys(), key=lambda c: -scores[c])[:3]
    sub_score = sum(scores[c] for c in ordered) or 1.0
    for i, cat in enumerate(ordered):
        if i == len(ordered) - 1:
            cut = min(caps[cat], rem)
        else:
            cut = min(caps[cat], round(needed * scores[cat] / sub_score))
        alloc[cat] = max(0, cut)
        rem -= alloc[cat]

    recs = [
        {
            "category": cat,
            "category_vi": CATEGORY_VI.get(cat, cat),
            "projected_remaining": caps[cat],
            "saving_amount": amt,
            "cut_pct": round(100 * amt / caps[cat]),
        }
        for cat, amt in alloc.items() if amt > 0
    ]
    selected = sum(r["saving_amount"] for r in recs)
    new_forecast = (forecast_data.get("forecast") or 0) - selected
    new_safe_daily = max(
        0,
        (forecast_data["budget_amount"] - forecast_data["spent"] - forecast_data["planned_essential"] + selected)
        // max(1, days_left),
    )

    return {
        "status": status,
        "target_saving": goal,
        "max_saving": max_saving,
        "selected_saving": selected,
        "remaining_gap": max(0, gap - selected),
        "new_forecast": new_forecast,
        "new_safe_to_spend_daily": new_safe_daily,
        "recommendations": recs,
        "locked_categories": forecast_data.get("protected_categories", []),
    }


@tool
def simulate_what_if(forecast_data: dict, adjustments: dict) -> dict:
    """simulate_what_if · Input: forecast_data và adjustments (vd {"food": 0.3, "amount_cut": 300000}) ·
    Output: dict chứa forecast mới, P50/P85 mới, gap mới và safe_to_spend_daily mới ·
    Không tác động ra ngoài."""
    if forecast_data.get("forecast") is None:
        return {"status": forecast_data.get("status"), "error": "Chưa có đường dự báo để mô phỏng What-If."}

    protected = set(forecast_data.get("protected_categories", []))
    flex_by_cat = forecast_data.get("flexible_by_category") or {}
    days_left = max(1, int(forecast_data.get("days_left") or 1))
    coverage = max(1, int(forecast_data.get("coverage_days") or 1))

    blocked = []
    saving = 0
    applied = {}
    for key, val in adjustments.items():
        if key == "amount_cut":
            saving += max(0, int(val))
            applied["amount_cut"] = max(0, int(val))
            continue
        if key in protected or key in ("housing", "health"):
            blocked.append(key)
            continue
        proj_cat = round(flex_by_cat.get(key, 0) * days_left / coverage)
        ratio = max(0.0, min(1.0, float(val)))
        cut = round(proj_cat * ratio)
        saving += cut
        applied[key] = {"cut_pct": round(ratio * 100), "saving_amount": cut}

    max_flex_proj = max(0, int(forecast_data.get("flexible_projection") or 0))
    saving = min(saving, max_flex_proj)
    new_forecast = forecast_data["forecast"] - saving
    new_p50 = max(forecast_data["spent"], (forecast_data.get("forecast_p50") or new_forecast) - saving)
    new_p85 = max(new_p50, (forecast_data.get("forecast_p85") or new_forecast) - saving)
    budget = forecast_data["budget_amount"]
    new_gap = max(0, max(forecast_data["spent"], new_forecast) - budget)
    new_status = "actual_over" if forecast_data["spent"] > budget else ("forecast_over" if new_forecast > budget else "safe")
    new_safe_daily = max(0, (budget - forecast_data["spent"] - forecast_data["planned_essential"] + saving) // days_left)

    return {
        "applied_adjustments": applied,
        "blocked_protected": blocked,
        "total_saving": saving,
        "new_status": new_status,
        "new_forecast": new_forecast,
        "new_forecast_p50": new_p50,
        "new_forecast_p85": new_p85,
        "new_gap": new_gap,
        "new_safe_to_spend_daily": new_safe_daily,
    }


def _parse_vnd(text: str) -> int | None:
    m = re.search(r"(\d[\d.,]*)\s*(tr|triệu|trieu|k|nghìn|ngàn|đ|d|vnd)?\b", text.lower())
    if not m:
        return None
    raw = m.group(1).replace(",", "").replace(".", "")
    if not raw.isdigit():
        return None
    num = int(raw)
    unit = m.group(2) or ""
    if unit in ("tr", "triệu", "trieu"):
        return num * 1_000_000
    if unit in ("k", "nghìn", "ngàn"):
        return num * 1_000
    return num


@tool
def ingest_transaction_draft(raw_text: str) -> dict:
    """ingest_transaction_draft · Input: câu nhập chi tiêu hoặc tin nhắn biến động số dư (str) ·
    Output: bản nháp giao dịch đã ẩn danh PII, gắn cờ is_transfer/is_reimbursable chờ người duyệt ·
    Không tác động ra ngoài (chỉ tạo bản nháp)."""
    lower = raw_text.lower()
    amounts = [_parse_vnd(part) for part in re.findall(r"\d[\d.,]*\s*(?:tr|triệu|trieu|k|nghìn|ngàn|đ|d|vnd)?", lower)]
    amounts = [a for a in amounts if a and a >= 1000]
    gross = amounts[0] if amounts else 0
    refund = amounts[1] if len(amounts) >= 2 and any(k in lower for k in ("hoàn", "trả lại", "chia", "gửi lại")) else 0

    is_transfer = any(k in lower for k in ("chuyển nội bộ", "sang momo", "sang ví", "tự chuyển"))
    is_reimbursable = refund > 0 or any(k in lower for k in ("trả hộ", "chia tiền", "campuchia"))
    net_amount = 0 if is_transfer else max(0, gross - refund)

    time_match = re.search(r"\b(\d{1,2})[:h](\d{2})?\b", lower)
    hour = int(time_match.group(1)) if time_match else None

    if is_transfer:
        category = "transfer"
    elif any(k in lower for k in ("trưa", "cơm", "ăn", "cà phê", "trà sữa", "đồ ăn", "khuya")):
        category = "food"
    elif hour is not None and (11 <= hour <= 13 or 21 <= hour <= 23) and 0 < net_amount <= 200_000:
        category = "food"
    elif any(k in lower for k in ("xe", "grab", "xăng", "gửi xe")):
        category = "transport"
    elif any(k in lower for k in ("thuốc", "khám", "y tế")):
        category = "health"
    elif any(k in lower for k in ("tiền nhà", "điện", "nước")):
        category = "housing"
    else:
        category = "other"

    return {
        "draft_status": "pending_user_approval",
        "requires_user_approval": True,
        "gross_amount": gross,
        "reimbursed_amount": refund,
        "net_amount": net_amount,
        "is_transfer": is_transfer,
        "is_reimbursable": is_reimbursable,
        "suggested_category": category,
        "suggested_category_vi": CATEGORY_VI.get(category, "Chuyển nội bộ" if category == "transfer" else category),
        "pii_stripped": True,
    }

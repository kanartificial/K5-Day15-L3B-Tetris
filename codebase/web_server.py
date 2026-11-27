"""HTTP API + static frontend cho FinPilot. Chạy bằng: python run.py"""
import json
import os
import sys
from datetime import date
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

import uuid
import csv
from datetime import date, datetime
from urllib.parse import parse_qs

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CODEBASE = os.path.dirname(os.path.abspath(__file__))
FRONTEND = os.path.join(CODEBASE, "frontend")
PROFILE_FILE = os.path.join(ROOT, "data", "user_profiles.json")

TRANSACTION_FILE = os.path.join(
    ROOT, "data", "user_transactions.json"
)

ALLOWED_CATEGORIES = {
    "food",
    "shopping",
    "entertainment",
    "transport",
    "travel",
    "housing",
    "health",
    "other"
}

def _load_profiles():
    try:
        with open(PROFILE_FILE, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def _save_profiles(profiles):
    os.makedirs(os.path.dirname(PROFILE_FILE), exist_ok=True)
    with open(PROFILE_FILE, "w", encoding="utf-8") as f:
        json.dump(profiles, f, ensure_ascii=False, indent=2)
sys.path.insert(0, CODEBASE)


def _load_user_transactions():
    try:
        with open(TRANSACTION_FILE, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _save_user_transactions(data):
    os.makedirs(os.path.dirname(TRANSACTION_FILE), exist_ok=True)

    with open(TRANSACTION_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _known_user(user_id):
    if user_id in _load_profiles():
        return True

    users_path = os.path.join(
        ROOT, "data", "synthetic", "users.csv"
    )

    try:
        with open(users_path, encoding="utf-8", newline="") as f:
            return any(
                row["user_id"] == user_id
                for row in csv.DictReader(f)
            )
    except FileNotFoundError:
        return False


def fallback_finpilot_reply(question, context=None):
    """
    FinPilot Assistant dự phòng.
    Không sử dụng API Key, không gọi LLM.
    Trả lời dựa trên dữ liệu tài chính thực tế.
    """
    import re

    q = question.lower().strip()
    context = context or {}
    forecast = context.get("forecast", context)

    budget = float(forecast.get("budget_amount") or 0)
    spent = float(forecast.get("spent") or 0)
    remaining = max(0, budget - spent)

    p50 = forecast.get("forecast_p50")
    p85 = forecast.get("forecast_p85")
    safe = forecast.get("safe_to_spend_daily")
    essential = forecast.get("essential_spent") or 0
    flexible = forecast.get("flexible_spent") or 0

    insufficient = (
        forecast.get("status") == "insufficient_data"
        or forecast.get("is_new_user", False)
        and spent == 0
    )

    def vnd(value):
        if value is None:
            return "Chưa đủ dữ liệu"
        return f"{value:,.0f} VNĐ"

    # 1. Hỏi tổng quan tài chính
    if any(k in q for k in [
        "tổng quan", "tình hình tài chính",
        "ngân sách", "đã chi", "còn bao nhiêu"
    ]):
        return (
            "Đây là tình hình tài chính hiện tại của bạn:\n\n"
            f"• Ngân sách tháng: {vnd(budget)}\n"
            f"• Đã chi tiêu: {vnd(spent)}\n"
            f"• Ngân sách còn lại: {vnd(remaining)}\n"
            f"• Chi thiết yếu: {vnd(essential)}\n"
            f"• Chi linh hoạt: {vnd(flexible)}\n\n"
            + (
                "Bạn chưa có đủ dữ liệu giao dịch để đánh giá xu hướng "
                "chi tiêu. Hãy thêm các khoản chi thực tế để FinPilot "
                "phân tích chính xác hơn."
                if insufficient else
                "Bạn nên tiếp tục theo dõi các khoản chi để kiểm soát "
                "ngân sách trong phần còn lại của tháng."
            )
        )

    # 2. Hỏi dự báo
    if any(k in q for k in [
        "dự báo", "cuối tháng", "p50", "p85",
        "vượt ngân sách", "nguy cơ"
    ]):
        if p50 is None or p85 is None:
            return (
                "Hiện tại FinPilot chưa có đủ dữ liệu lịch sử để đưa ra "
                "dự báo P50 và P85 đáng tin cậy.\n\n"
                f"Ngân sách tháng: {vnd(budget)}\n"
                f"Đã chi: {vnd(spent)}\n"
                f"Còn lại: {vnd(remaining)}\n\n"
                "Bạn hãy tiếp tục ghi nhận giao dịch thực tế. "
                "Hệ thống sẽ đánh giá dự báo khi đạt điều kiện dữ liệu."
            )

        return (
            "Kết quả dự báo chi tiêu cuối tháng:\n\n"
            f"• P50: {vnd(p50)}\n"
            f"• P85: {vnd(p85)}\n"
            f"• Ngân sách: {vnd(budget)}\n\n"
            + (
                "Dự báo cho thấy có nguy cơ vượt ngân sách. "
                "Bạn nên ưu tiên kiểm soát các khoản chi linh hoạt."
                if float(p85) > budget else
                "Theo dự báo P85, chi tiêu vẫn nằm trong giới hạn "
                "ngân sách hiện tại."
            )
        )

    # 3. Hỏi tiết kiệm
    if any(k in q for k in [
        "tiết kiệm", "cắt giảm", "giảm chi",
        "nên làm gì", "tối ưu"
    ]):
        return (
            "Một số gợi ý kiểm soát chi tiêu:\n\n"
            f"1. Theo dõi khoản chi linh hoạt hiện tại: {vnd(flexible)}.\n"
            "2. Ưu tiên xem xét mua sắm và giải trí trước khi "
            "điều chỉnh các khoản thiết yếu.\n"
            "3. Không cắt giảm các danh mục bạn đã đánh dấu cần bảo vệ.\n"
            f"4. Duy trì mức chi tiêu trung bình không vượt "
            f"{vnd(safe)} mỗi ngày nếu đây là Safe-to-Spend hợp lệ.\n\n"
            "Đây là các gợi ý quản lý tài chính chung, không phải "
            "kết quả tối ưu hóa bằng mô hình AI."
        )

    # 4. Hỏi Safe-to-Spend
    if any(k in q for k in [
        "safe-to-spend", "mỗi ngày", "mỗi ngày được chi",
        "chi tiêu hàng ngày"
    ]):
        if safe is None:
            return (
                "FinPilot chưa thể xác định mức chi tiêu mỗi ngày "
                "do chưa có đủ dữ liệu hoặc thông tin thời gian."
            )

        return (
            f"Mức Safe-to-Spend hiện tại là {vnd(safe)}/ngày.\n\n"
            "Đây là mức tham khảo dựa trên ngân sách còn lại và "
            "thời gian còn lại của kỳ ngân sách. Bạn nên ưu tiên "
            "các khoản chi thiết yếu."
        )

    # 5. Hỏi dữ liệu thiếu
    if insufficient:
        return (
            "Chào bạn! Mình là FinPilot Assistant.\n\n"
            "Hồ sơ hiện chưa có đủ lịch sử giao dịch để thực hiện "
            "phân tích chuyên sâu.\n\n"
            "Bạn có thể bắt đầu bằng cách:\n"
            "• Thêm các khoản chi đã phát sinh.\n"
            "• Theo dõi tổng chi tiêu so với ngân sách.\n"
            "• Phân loại khoản chi thiết yếu và linh hoạt.\n\n"
            "Khi có đủ dữ liệu, hệ thống sẽ hỗ trợ đánh giá xu hướng "
            "và dự báo chi tiêu."
        )

    # 6. Câu hỏi khác
    return (
        "Mình là FinPilot Assistant, trợ lý hỗ trợ quản lý "
        "tài chính cá nhân.\n\n"
        "Mình hiện có thể hỗ trợ bạn theo các nhóm thông tin:\n"
        "• Tổng quan ngân sách và khoản đã chi.\n"
        "• Dự báo chi tiêu P50/P85 khi đủ dữ liệu.\n"
        "• Safe-to-Spend mỗi ngày.\n"
        "• Gợi ý kiểm soát và tiết kiệm chi tiêu.\n\n"
        "Bạn hãy thử hỏi: \"Tháng này mình đã chi bao nhiêu?\" "
        "hoặc \"Mình có nguy cơ vượt ngân sách không?\""
    )


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=FRONTEND, **kwargs)

    def _json(self, payload, status=200):
        raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(raw)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/health":
            return self._json({"ok": True, "service": "FinPilot API"})
        if path == "/api/profiles":
            profiles = _load_profiles()
            return self._json({"profiles": [{"user_id": k, "name": v.get("name", k)} for k, v in profiles.items()]})

        if path == "/api/transactions":
            params = parse_qs(urlparse(self.path).query)

            user_id = params.get("user_id", ["U010"])[0]
            month = params.get(
                "month", [date.today().strftime("%Y-%m")]
            )[0]

            if not _known_user(user_id):
                return self._json(
                    {"error": "Không tìm thấy người dùng."}, 404
                )

            from tools import _load_synthetic_snapshot

            profiles = _load_profiles()

            if user_id in profiles:
                rows = [
                    x for x in profiles[user_id].get("transactions", [])
                    if x.get("transaction_date", "")[:7] == month
                ]
            else:
                snapshot = _load_synthetic_snapshot(
                    user_id, month, date.today().isoformat()
                )
                rows = snapshot.get("transactions", [])

            manual = _load_user_transactions().get(user_id, [])

            rows += [
                x for x in manual
                if x.get("transaction_date", "")[:7] == month
            ]

            return self._json({
                "user_id": user_id,
                "month": month,
                "transactions": rows
            })
        
        if path == "/api/overview":
            try:
                from tools import (
                    get_cashflow_forecast,
                    optimize_budget_reduction,
                    _load_synthetic_snapshot
                )

                params = parse_qs(urlparse(self.path).query)

                user_id = params.get("user_id", ["U010"])[0]
                month = params.get(
                    "month", [date.today().strftime("%Y-%m")]
                )[0]

                today = date.today()
                profiles = _load_profiles()

                manual = _load_user_transactions().get(user_id, [])

                if user_id in profiles:
                    profile = profiles[user_id]

                    rows = list(profile.get("transactions", []))

                    rows += [
                        x for x in manual
                        if x.get("transaction_date", "")[:7] == month
                    ]

                    dates = [
                        x["transaction_date"]
                        for x in rows
                        if x.get("transaction_date", "").startswith(month)
                    ]

                    first_date = min(dates) if dates else None

                    coverage = (
                        (today - date.fromisoformat(first_date)).days + 1
                        if first_date else 0
                    )

                    payload = {
                        "month": month,
                        "as_of": today.isoformat(),
                        "coverage_days": coverage,
                        "budget_amount": int(profile["monthly_budget"]),
                        "protected_categories": profile.get(
                            "protected_categories", []
                        ),
                        "transactions": rows,
                        "planned_expenses": []
                    }

                    forecast = get_cashflow_forecast(
                        payload_json=json.dumps(payload, ensure_ascii=False)
                    )

                    forecast["income_amount"] = profile.get(
                        "monthly_income", 0
                    )

                    forecast["current_balance"] = profile.get(
                        "current_balance", 0
                    )

                    forecast["is_new_user"] = True
                    forecast["profile"] = profile

                else:
                    payload = _load_synthetic_snapshot(
                        user_id, month, today.isoformat()
                    )

                    payload["transactions"].extend([
                        x for x in manual
                        if x.get("transaction_date", "")[:7] == month
                    ])

                    forecast = get_cashflow_forecast(
                        payload_json=json.dumps(payload, ensure_ascii=False)
                    )

                    forecast["is_new_user"] = False

                optimization = (
                    optimize_budget_reduction(forecast)
                    if forecast.get("gap", 0)
                    and forecast.get("status") != "insufficient_data"
                    else None
                )

                return self._json({
                    "forecast": forecast,
                    "optimization": optimization,
                    "user_id": user_id,
                    "month": forecast.get("month", month)
                })
            except Exception as exc:
                return self._json({"error": str(exc)}, 500)
        return super().do_GET()

    def do_POST(self):
        path = urlparse(self.path).path
        try:
            length = int(self.headers.get("Content-Length", "0"))
            body = json.loads(self.rfile.read(length).decode("utf-8"))
            if path == "/api/onboarding":
                name = str(body.get("name", "")).strip()
                income = int(body.get("monthly_income", 0))
                budget = int(body.get("monthly_budget", 0))
                balance = int(body.get("current_balance", 0))
                if not name or income <= 0 or budget <= 0 or budget > income or balance < 0:
                    return self._json({"error": "Vui lòng nhập tên, thu nhập và ngân sách hợp lệ. Ngân sách không được lớn hơn thu nhập."}, 400)
                profiles = _load_profiles()
                user_id = "NEW%03d" % (len(profiles) + 1)
                profiles[user_id] = {
                    "name": name, "monthly_income": income, "monthly_budget": budget,
                    "current_balance": balance,
                    "protected_categories": body.get("protected_categories") or ["housing", "health"],
                    "transactions": []
                }
                _save_profiles(profiles)
                return self._json({"ok": True, "user_id": user_id, "profile": profiles[user_id]}, 201)
            
            if path == "/api/transactions":
                user_id = str(body.get("user_id", "")).strip()
                description = str(body.get("description", "")).strip()
                category = str(body.get("category", "")).strip()
                tx_date = str(body.get("transaction_date", "")).strip()

                try:
                    amount = int(body.get("amount", 0))
                    datetime.strptime(tx_date, "%Y-%m-%d")
                except (TypeError, ValueError):
                    return self._json({
                        "error": "Số tiền hoặc ngày giao dịch không hợp lệ."
                    }, 400)

                if not _known_user(user_id):
                    return self._json({
                        "error": "Không tìm thấy người dùng."
                    }, 404)

                if not description or len(description) > 100:
                    return self._json({
                        "error": "Tên khoản chi phải từ 1 đến 100 ký tự."
                    }, 400)

                if amount <= 0:
                    return self._json({
                        "error": "Số tiền phải lớn hơn 0."
                    }, 400)

                if category not in ALLOWED_CATEGORIES:
                    return self._json({
                        "error": "Danh mục không hợp lệ."
                    }, 400)

                today = date.today()
                parsed_date = date.fromisoformat(tx_date)

                if parsed_date > today:
                    return self._json({
                        "error": "Ngày giao dịch không được ở tương lai."
                    }, 400)

                if tx_date[:7] != today.strftime("%Y-%m"):
                    return self._json({
                        "error": "Demo hiện chỉ ghi nhận giao dịch trong tháng hiện tại."
                    }, 400)

                profiles = _load_profiles()

                protected = profiles.get(
                    user_id, {}
                ).get("protected_categories", [])

                transaction = {
                    "transaction_id": "MANUAL-" + uuid.uuid4().hex[:12].upper(),
                    "transaction_date": tx_date,
                    "amount": amount,
                    "category": category,
                    "is_essential": (
                        bool(body.get("is_essential", False))
                        or category in protected
                    ),
                    "transaction_type": "expense",
                    "related_transaction_id": None,
                    "description": description
                }

                all_transactions = _load_user_transactions()

                all_transactions.setdefault(user_id, []).append(
                    transaction
                )

                _save_user_transactions(all_transactions)

                return self._json({
                    "ok": True,
                    "transaction": transaction
                }, 201)
            
            if path == "/api/whatif":
                from tools import get_cashflow_forecast, simulate_what_if
                user_id = str(body.get("user_id", "U010"))
                adjustments = body.get("adjustments") or {}
                allowed = {"food", "shopping", "entertainment", "transport", "travel", "other"}
                adjustments = {k: max(0, min(1, float(v))) for k, v in adjustments.items() if k in allowed}
                forecast = get_cashflow_forecast(
                    payload_json=json.dumps(payload, ensure_ascii=False)
                )

                result = simulate_what_if(forecast, adjustments)

                return self._json({
                    "forecast": forecast,
                    "simulation": result
                })


            if path == "/api/chat":
                message = str(body.get("message", "")).strip()
                context = body.get("financial_context", {})
                
                if not message:
                    return self._json({
                        "error": "Vui lòng nhập câu hỏi."
                    }, 400)

                try:
                    from agent import answer

                    result = answer(message)

                    # Chuẩn hóa kết quả từ Agent
                    if isinstance(result, dict):
                        reply = (
                            result.get("answer")
                            or result.get("response")
                            or result.get("reply")
                            or str(result)
                        )
                    else:
                        reply = str(result)

                    return self._json({
                        "reply": reply,
                        "mode": "agent",
                        "trace": {}
                    })

                except Exception as e:
                    # Không để lỗi API làm hỏng trải nghiệm người dùng
                    print(f"[FinPilot] Agent unavailable: {e}")

                    reply = fallback_finpilot_reply(
                        message,
                        context
                    )

                    return self._json({
                        "reply": reply,
                        "mode": "fallback",
                        "trace": {
                            "model_calls": 0,
                            "tool_calls": 0,
                            "tokens_in": 0,
                            "tokens_out": 0
                        }
                    })

            
            if path != "/api/chat":
                return self._json({"error": "Endpoint không tồn tại"}, 404)
            message = str(body.get("message", "")).strip()
            if not message:
                return self._json({"error": "Vui lòng nhập câu hỏi."}, 400)

            import tracing
            from agent import answer
            tracing.begin("web-chat")
            try:
                result = answer(message)
                summary, events = tracing.end()
            except Exception:
                tracing.end()
                raise

            return self._json({
                "reply": result.get("output", str(result)),
                "trace": summary,
                "events": events,
            })
        except NotImplementedError as exc:
            return self._json({"error": "Model chưa được kết nối: " + str(exc)}, 503)
        except Exception as exc:
            return self._json({"error": type(exc).__name__ + ": " + str(exc)}, 500)

    def log_message(self, fmt, *args):
        print("[FinPilot] " + fmt % args)


def main():
    host = os.environ.get("FINPILOT_HOST", "127.0.0.1")
    port = int(os.environ.get("FINPILOT_PORT", "8000"))
    server = ThreadingHTTPServer((host, port), Handler)
    print("FinPilot đang chạy tại http://%s:%s" % (host, port))
    print("Nhấn Ctrl+C để dừng.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\\nĐang dừng FinPilot...")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()

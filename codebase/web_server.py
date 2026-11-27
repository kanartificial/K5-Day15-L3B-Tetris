"""HTTP API + static frontend cho FinPilot. Chạy bằng: python run.py"""
import json
import os
import sys
from datetime import date
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CODEBASE = os.path.dirname(os.path.abspath(__file__))
FRONTEND = os.path.join(CODEBASE, "frontend")
sys.path.insert(0, CODEBASE)


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
        if path == "/api/overview":
            try:
                from tools import get_cashflow_forecast, optimize_budget_reduction
                query = urlparse(self.path).query
                params = dict(x.split("=", 1) for x in query.split("&") if "=" in x)
                user_id = params.get("user_id", "U010")
                month = params.get("month", "2026-11")
                # Snapshot demo trong repo được cập nhật đến 20/11/2026.
                forecast = get_cashflow_forecast(user_id=user_id, month=month, as_of="2026-11-20")
                optimization = optimize_budget_reduction(forecast) if forecast.get("gap", 0) > 0 else None
                return self._json({"forecast": forecast, "optimization": optimization,
                                   "user_id": user_id, "month": month})
            except Exception as exc:
                return self._json({"error": str(exc)}, 500)
        return super().do_GET()

    def do_POST(self):
        path = urlparse(self.path).path
        try:
            length = int(self.headers.get("Content-Length", "0"))
            body = json.loads(self.rfile.read(length).decode("utf-8"))
            if path == "/api/whatif":
                from tools import get_cashflow_forecast, simulate_what_if
                user_id = str(body.get("user_id", "U010"))
                adjustments = body.get("adjustments") or {}
                allowed = {"food", "shopping", "entertainment", "transport", "travel", "other"}
                adjustments = {k: max(0, min(1, float(v))) for k, v in adjustments.items() if k in allowed}
                forecast = get_cashflow_forecast(user_id=user_id, month="2026-11", as_of="2026-11-20")
                result = simulate_what_if(forecast, adjustments)
                return self._json({"forecast": forecast, "simulation": result})
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

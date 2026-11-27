"""Nối model — chỗ DUY NHẤT trong bản chạy thử gọi model AI. NHÓM VIẾT phần gọi model thật.

Hợp đồng (giữ nguyên để khung đo được token):
    call_model(system: str, user: str) -> dict với 4 khoá
        "text":       str   chữ model trả về
        "model":      str   tên model đã gọi (để tra giá ở bảng giá model)
        "tokens_in":  int   số token vào, lấy từ trường usage trong phản hồi API — KHÔNG ước lượng
        "tokens_out": int   số token ra, gồm cả token suy luận / suy nghĩ nếu API tính riêng
    @model_call (từ tracing.py) tự ghi mỗi lần gọi vào trace; agent.py gọi call_model bao nhiêu lần
    cũng được, khung tự cộng token.
    Lỗi gọi model (hết lượt, sai key, mất mạng): cứ để exception bay ra — khung ghi lỗi vào cột error.

Chế độ giả (mặc định khi .env chưa có MODEL_PROVIDER, hoặc MODEL_PROVIDER=fake):
    trả một câu giả cố định, model "fake", token 0 — để luồng chạy hết từ trước CP2 (guide bước 3.2).
    Lượt `run.py eval` / `run.py simulate` chạy bằng model giả KHÔNG được tính.

Nối model thật: điền .env (chép từ .env.example), rồi chạy `python run.py eval --try`.
"""
import json
import os
import urllib.error
import urllib.request

from tracing import model_call

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_env(path=os.path.join(ROOT, ".env")):
    """Đọc file .env (KEY=VALUE mỗi dòng) vào biến môi trường, không ghi đè biến đã có. Khung — không cần sửa."""
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env()
MODEL_PROVIDER = (os.environ.get("MODEL_PROVIDER") or "fake").strip().lower()
MODEL_NAME = (os.environ.get("MODEL_NAME") or "").strip()
API_KEY = (os.environ.get("API_KEY") or "").strip()
BASE_URL = (os.environ.get("BASE_URL") or "").strip()

SHOW_RAW = False
URL_OPENAI = "https://api.openai.com/v1/chat/completions"
URL_CLAUDE = "https://api.anthropic.com/v1/messages"
URL_OLLAMA = "http://localhost:11434/api/chat"


def _post_json(url: str, headers: dict, body: dict, timeout: int = 60) -> dict:
    """Gửi POST JSON bằng thư viện chuẩn và trả về JSON phản hồi."""
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        method="POST",
        headers={"Content-Type": "application/json", **headers},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise RuntimeError("HTTP %d: %s" % (e.code, e.read().decode("utf-8", "replace")[:300]))
    if SHOW_RAW:
        print(json.dumps(data, ensure_ascii=False, indent=2)[:3000])
    return data


def _require_config() -> None:
    if not MODEL_NAME:
        raise RuntimeError("Thiếu MODEL_NAME trong .env")
    if MODEL_PROVIDER != "ollama" and not API_KEY:
        raise RuntimeError("Thiếu API_KEY trong .env cho MODEL_PROVIDER=%s" % MODEL_PROVIDER)


def _call_openai(system: str, user: str) -> dict:
    messages = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": user}]
    url = BASE_URL or URL_OPENAI
    data = _post_json(
        url,
        {"Authorization": "Bearer " + API_KEY},
        {"model": MODEL_NAME, "messages": messages},
    )
    usage = data["usage"]
    return {
        "text": data["choices"][0]["message"]["content"],
        "tokens_in": int(usage["prompt_tokens"]),
        "tokens_out": int(usage["completion_tokens"]),
    }


def _call_claude(system: str, user: str) -> dict:
    data = _post_json(
        BASE_URL or URL_CLAUDE,
        {"x-api-key": API_KEY, "anthropic-version": "2023-06-01"},
        {
            "model": MODEL_NAME,
            "max_tokens": 1024,
            "system": system or "",
            "messages": [{"role": "user", "content": user}],
        },
    )
    text = "".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text")
    usage = data["usage"]
    return {
        "text": text,
        "tokens_in": int(usage["input_tokens"]),
        "tokens_out": int(usage["output_tokens"]),
    }


def _call_gemini(system: str, user: str) -> dict:
    model_path = MODEL_NAME if MODEL_NAME.startswith("models/") else f"models/{MODEL_NAME}"
    url = BASE_URL or f"https://generativelanguage.googleapis.com/v1beta/{model_path}:generateContent"
    body = {"contents": [{"role": "user", "parts": [{"text": user}]}]}
    if system:
        body["system_instruction"] = {"parts": [{"text": system}]}
    data = _post_json(url, {"x-goog-api-key": API_KEY}, body)
    parts = data["candidates"][0]["content"].get("parts", [])
    text = "".join(p.get("text", "") for p in parts if "text" in p)
    usage = data["usageMetadata"]
    tokens_in = int(usage["promptTokenCount"])
    tokens_out = int(usage.get("candidatesTokenCount", 0)) + int(usage.get("thoughtsTokenCount", 0))
    return {"text": text, "tokens_in": tokens_in, "tokens_out": tokens_out}


def _call_ollama(system: str, user: str) -> dict:
    messages = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": user}]
    data = _post_json(
        BASE_URL or URL_OLLAMA,
        {},
        {"model": MODEL_NAME, "messages": messages, "stream": False},
        timeout=300,
    )
    return {
        "text": data["message"]["content"],
        "tokens_in": int(data.get("prompt_eval_count", 0)),
        "tokens_out": int(data.get("eval_count", 0)),
    }


@model_call
def call_model(system: str, user: str) -> dict:
    if MODEL_PROVIDER == "fake":
        last = (user.strip().splitlines() or [""])[-1]
        return {"text": "[câu trả lời giả — chưa nối model] " + last[:60], "model": "fake", "tokens_in": 0, "tokens_out": 0}

    _require_config()
    if MODEL_PROVIDER in ("openai", "openai_compatible", "deepseek", "openrouter"):
        result = _call_openai(system, user)
    elif MODEL_PROVIDER in ("anthropic", "claude"):
        result = _call_claude(system, user)
    elif MODEL_PROVIDER in ("gemini", "google"):
        result = _call_gemini(system, user)
    elif MODEL_PROVIDER == "ollama":
        result = _call_ollama(system, user)
    else:
        raise NotImplementedError(
            "Chưa hỗ trợ MODEL_PROVIDER=%s trong codebase/ai.py — xem docs/connect-model.md" % MODEL_PROVIDER
        )

    return {
        "text": result["text"],
        "model": MODEL_NAME,
        "tokens_in": int(result["tokens_in"]),
        "tokens_out": int(result["tokens_out"]),
    }

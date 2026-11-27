"""Đếm review theo chủ đề. Chạy sau scrape_reviews.py:  python evidence/count_reviews.py

Mẫu số: review "có nội dung" = ≥8 từ, bỏ spam quảng cáo vay (có "vay" + ".com"/"c0m").
Mỗi chủ đề là một regex (không phân biệt hoa thường); một review có thể thuộc nhiều chủ đề.
Lọc bằng từ khoá chỉ ra ỨNG VIÊN — các nhóm pain (P*) được đọc tay lại, xem evidence/data-mining.md.
In thêm: --show P2  → in nguyên văn các review khớp chủ đề đó.
"""
import csv
import pathlib
import re
import sys
import unicodedata

TOPICS = {
    # pain liên quan lát cắt
    "P1 nhắc ngân sách/hạn mức": r"ngân sách|ngan sach|budget|hạn mức",
    "P2 cảnh báo/nhắc khi vượt": r"(cảnh báo|thông báo|nhắc|báo động|alert).{0,40}(vượt|quá|ngân sách|hạn mức|hết tiền)"
                                 r"|(vượt|quá|ngân sách|hạn mức).{0,40}(cảnh báo|thông báo|nhắc|báo động)",
    "P3 kể chi quá tay/hết tiền": r"chi quá|tiêu quá|quá tay|hết tiền|cháy túi|thâm hụt|thiếu tiền|vượt (quá )?(mức|ngân sách|hạn mức|chi)|tiêu lố|chi lố",
    "P4 muốn gợi ý/tư vấn cắt giảm": r"gợi ý|tư vấn|cắt giảm|lời khuyên|\bAI\b",
    "P5 giá trị: biết/kiểm soát chi tiêu": r"kiểm soát|biết (được )?(mình )?(đã )?(chi|tiêu)|tiêu (vào )?(gì|đâu)|tiền đi đâu",
    # chủ đề nền, để so tỷ lệ
    "N1 lỗi/mất dữ liệu": r"lỗi|mất (hết )?dữ liệu|văng|crash|không (vào|đăng nhập|lưu)",
    "N2 quảng cáo": r"quảng cáo|\bqc\b",
    "N3 trả phí/premium": r"trả phí|trả tiền|premium|nâng cấp|thành viên|vip",
    "N4 liên kết ngân hàng/đồng bộ": r"liên kết|ngân hàng|đồng bộ|sync|sao lưu|backup",
}

# Gán nhãn TAY sau khi đọc toàn bộ review khớp P1–P5 (mã = 8 ký tự đầu sha1 của reviewId).
LABELS = {
    "L1 muốn được cảnh báo / chia nhịp chi khi sắp vượt": ["7c6412de", "b38091c9", "e73ca5a3", "04981bfa", "9adfff0b"],
    "L2 muốn gợi ý / lời khuyên cân đối chi tiêu": ["9c0eb30d"],
    "L3 kể không biết tiền đi đâu / hết tiền trước cuối tháng": ["36c8e675", "a9a8b971", "9d0c8d54", "eeebf07c", "d9364644", "fa7cbaf9"],
}

path = pathlib.Path(__file__).with_name("raw-reviews.csv")
rows = list(csv.DictReader(path.open(encoding="utf-8-sig")))
spam = re.compile(r"vay.*(\.|\s)c[o0]m|vay\s*(onl|tốt|totnhat)|vaytotnhat", re.I)
is_spam = lambda t: bool(spam.search(unicodedata.normalize("NFKC", t)))
base = [r for r in rows if len(r["noi_dung"].split()) >= 8 and not is_spam(r["noi_dung"])]
n = len(base)
print(f"Tổng review cào: {len(rows)} · có nội dung (mẫu số N): {n}")
print(f"Khoảng ngày: {min(r['ngay'] for r in base)} → {max(r['ngay'] for r in base)}\n")

show = sys.argv[sys.argv.index("--show") + 1] if "--show" in sys.argv else None
for name, pat in TOPICS.items():
    rx = re.compile(pat, re.I)
    hit = [r for r in base if rx.search(r["noi_dung"])]
    print(f"{name:40s} {len(hit):5d}/{n} ({len(hit) / n:.1%})")
    if show and name.startswith(show + " "):
        for r in hit:
            print(f"    [{r['ma']}] {r['app']} · {r['ngay']} · {r['sao']}★ · {r['noi_dung']}")

codes = {r["ma"] for r in base}
print("\n--- nhãn tay ---")
all_codes = set()
for name, ids in LABELS.items():
    ok = [i for i in ids if i in codes]
    all_codes |= set(ok)
    print(f"{name:55s} {len(ok):3d}/{n} ({len(ok) / n:.2%})")
print(f"{'Hợp (ít nhất 1 nhãn)':55s} {len(all_codes):3d}/{n} ({len(all_codes) / n:.2%})")

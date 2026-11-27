"""Cào review công khai trên Google Play của các app quản lý chi tiêu (Track E).

Chạy:  python evidence/scrape_reviews.py
Ra:    evidence/raw-reviews.csv  (bị .gitignore chặn, KHÔNG commit — repo chỉ giữ số tổng hợp + vài ví dụ)
Cần:   python -m pip install google-play-scraper

Không lưu tên / ảnh người viết review. Mã review được rút gọn thành hash 8 ký tự.
"""
import csv
import hashlib
import pathlib

from google_play_scraper import Sort, reviews

APPS = {
    "com.bookmark.money": "Money Lover",
    "vn.com.misa.sothuchi": "Sổ Thu Chi MISA",
    "com.freeman.moneymanager": "Sổ thu chi (Freeman)",
    "com.realbyteapps.moneymanagerfree": "Money Manager (Realbyte)",
    "cashbook.cashbook": "Sổ Chi Tiêu (Cashbook)",
    "com.droid4you.application.wallet": "Wallet",
    "com.blodhgard.easybudget": "Quản lý Ngân sách Chi tiêu",
    "com.zotiger.accountbook": "Money+",
}
PER_APP = 1000  # review mới nhất mỗi app

out = pathlib.Path(__file__).with_name("raw-reviews.csv")
with out.open("w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["ma", "app", "ngay", "sao", "luot_huu_ich", "noi_dung"])
    for app_id, name in APPS.items():
        got, token = [], None
        while len(got) < PER_APP:
            batch, token = reviews(app_id, lang="vi", country="vn", sort=Sort.NEWEST,
                                   count=min(200, PER_APP - len(got)), continuation_token=token)
            got += batch
            if not batch or token is None or token.token is None:
                break
        for r in got:
            text = (r["content"] or "").replace("\n", " ").strip()
            if not text:
                continue
            ma = hashlib.sha1(r["reviewId"].encode()).hexdigest()[:8]
            w.writerow([ma, name, r["at"].date().isoformat(), r["score"], r["thumbsUpCount"], text])
        print(f"{name}: {len(got)} review")
print("→", out)

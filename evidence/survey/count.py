"""Đếm kết quả khảo sát từ results.csv. Chạy: python evidence/survey/count.py"""
import collections
import csv
import pathlib

MULTI = ("7.", "10.", "17.", "18.")  # câu chọn nhiều, đáp án nối bằng ", "

path = pathlib.Path(__file__).with_name("results.csv")
rows = list(csv.DictReader(path.open(encoding="utf-8-sig")))
n = len(rows)
print(f"n = {n}\n")

for col in rows[0]:
    if col in ("phieu", "Dấu thời gian"):
        continue
    cnt = collections.Counter()
    for r in rows:
        values = r[col].split(", ") if col.startswith(MULTI) else [r[col]]
        cnt.update(v or "(trống)" for v in values)
    print(col)
    for k, v in cnt.most_common():
        print(f"    {v}/{n}  {k}")

# Số ghép dùng trong evidence/summary.md
q5 = next(c for c in rows[0] if c.startswith("5."))
q8 = next(c for c in rows[0] if c.startswith("8."))
q9 = next(c for c in rows[0] if c.startswith("9."))
print("\n--- số ghép ---")
print(f"Vượt ngân sách >=1 tháng / 3 tháng: {sum(r[q5] in ('1 tháng','2 tháng','3 tháng') for r in rows)}/{n}")
print(f"Nhận ra muộn (cuối tháng / gần hết tiền / không theo dõi): "
      f"{sum(r[q8] in ('Cuối tháng','Khi gần hết tiền','Không theo dõi / Không áp dụng') for r in rows)}/{n}")
print(f"Thiếu tiền thường xuyên hoặc thỉnh thoảng: {sum(r[q9] in ('Thường xuyên','Thỉnh thoảng') for r in rows)}/{n}")

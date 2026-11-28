# Tóm tắt mô phỏng simulate-1@20261128-121402

Do `python run.py simulate` sinh ra — không sửa tay. Chép bảng sang `cost/cost-estimate.md`.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| dung_it | 24 | 1 | 558 | 229 | 1.0 | 0.8 |
| dung_vua | 13 | 2 | 1019 | 562 | 2.0 | 1.2 |
| dung_nhieu | 7 | 3 | 1918 | 940 | 3.0 | 3.6 |

Tỉ lệ đạt dùng để tính: 28/30 (93%) — lượt run-2@20261128-102508

- Tự chọn: lượt run-N mới nhất đã chấm xong, chạy bằng đúng model đang đo (run-2.csv). Muốn dùng lượt khác (vd lượt 2): thêm `--rate-from eval/run-2.csv`.

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (100 người) | Chi phí / tháng — cơ sở (500 người) | Chi phí / tháng — cao (1.000 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| gpt-6-luna (vào 0.1 · ra 0.5 $/1M) | $0.00031 | $0.00033 | $0.00021 | $0.2088 | $1.04 | $2.09 | $0.0021 |
| gpt-6.2-sol (vào 2.0 · ra 10.0 $/1M) | $0.0062 | $0.0067 | $0.0041 | $4.18 | $20.88 | $41.76 | $0.0418 |

- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Chi phí / câu hỏi đạt = chi phí / phiên ÷ số lượt hỏi trung bình mỗi phiên (1.6) ÷ tỉ lệ đạt — tỉ lệ đạt đo theo từng câu thử.
- Token đo trên model: gpt-6-luna. Giá tính theo từng model trong bảng — model khác bộ tách token thì số token thật có thể lệch; ghi rõ "đo trên model X, tính giá model Y" trong cost/cost-estimate.md.
- Phiên lỗi (không tính vào trung bình): 6/50.

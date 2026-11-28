# Chi phí khi dùng thật

> Điền ở guide bước 4.2, nộp ở CP4 14:30 Thứ Bảy 28/11. Ôn lại: ngày 13, ngày 1, ngày 14 · lab ngày 13, lab ngày 14. Chấm ở rubric R6.
> Số **không điền tay**: điền `cost/personas.yaml` → `python run.py simulate` → chép bảng trong `cost/simulate-N-summary.md` vào đây.
> Lúc build dùng gói miễn phí vẫn tính theo **giá gói trả phí** — đây là chi phí cho lúc đưa vào dùng thật.
## 1. Đầu vào

- **Persona** (`cost/personas.yaml`): 3 kiểu — `dung_it` (50%, 4 phiên/người/tháng, 1 lượt hỏi/phiên); `dung_vua` (30%, 6 phiên/người/tháng, 2 lượt hỏi/phiên); `dung_nhieu` (20%, 8 phiên/người/tháng, 3 lượt hỏi/phiên). Nguồn: Khảo sát người dùng Q4 (21 phản hồi) dùng để xác định nhu cầu; tỉ lệ persona và tần suất sử dụng là tự ước tính.
- **Số người dùng thật** 3 kịch bản: thấp 100 · cơ sở 500 · cao 1.000. Nguồn: Giả định quy mô triển khai để mô phỏng, không phải số liệu người dùng thực tế.
- **Giá** ≥2 mức model (từ `further-reading/model-prices.md` của repo gốc đề bài):
  - `gpt-6-luna`: Input $0.10, Output $0.50, Cached Input $0.01 / 1 triệu token.
  - `gpt-6.2-sol`: Input $2.00, Output $10.00 / 1 triệu token.
  - Nguồn: https://developers.openai.com/api/docs/models — ngày xem 28/11/2026.
- **Tỉ lệ đạt** dùng để tính: 28/30 (93%) — lượt `run-2@20261128-102508` (lượt 2).
- Đo token trên model `gpt-6-luna`, tính giá model `gpt-6-luna` và `gpt-6.2-sol`.

## 2. Kết quả mô phỏng

Lượt mô phỏng: `cost/simulate-1.csv` · run ID `simulate-1@20261128-121402` · 50 phiên (44 hợp lệ, 6 lỗi) · seed 42.

### Thống kê theo persona

| Persona | Số phiên hợp lệ | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| dung_it | 24 | 1 | 558 | 229 | 1.0 | 0.8 |
| dung_vua | 13 | 2 | 1019 | 562 | 2.0 | 1.2 |
| dung_nhieu | 7 | 3 | 1918 | 940 | 3.0 | 3.6 |

### Chi phí theo model

| Model | Chi phí / phiên | Chi phí / task thành công | / tháng — thấp | / tháng — cơ sở | / tháng — cao | / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|
| gpt-6-luna | $0.00031 | $0.00033 | $0.2088 | $1.04 | $2.09 | $0.0021 |
| gpt-6.2-sol | $0.0062 | $0.0067 | $4.18 | $20.88 | $41.76 | $0.0418 |

Chi phí / task thành công = chi phí trung bình mỗi phiên ÷ tỉ lệ đạt 93%.

## 3. So với impact

- **Impact / người / tháng** (`spec.md` §2): **12 người × 6 lượt/người/tháng × 15 phút/lượt = 1.080 phút (18 giờ)/tháng**
- **Chi phí / người / tháng** (cơ sở, model `gpt-6-luna`): $0.0021.
- **Chi phí / người / tháng** (cơ sở, model `gpt-6.2-sol`): $0.0418.
- **Kết luận một dòng — đáng làm không:** Đáng triển khai thử nghiệm vì chi phí AI ước tính trên mỗi người dùng tương đối thấp; `gpt-6-luna` phù hợp làm model chính, còn `gpt-6.2-sol` là phương án đối chiếu chất lượng với chi phí cao hơn khoảng 19,9 lần.

## 4. Phân tích bổ sung

- **Cache:** Có thể giảm chi phí input khi tái sử dụng nội dung ngữ cảnh, system prompt; cần đo riêng cached tokens để xác định mức tiết kiệm thực tế.
- **Cắt ngữ cảnh:** Giới hạn lịch sử hội thoại và chỉ đưa dữ liệu giao dịch liên quan vào prompt để giảm token đầu vào.
- **Giới hạn bước:** Giới hạn số lần gọi model và tool trong một phiên để kiểm soát chi phí.
- **Chi phí ngoài model:** Chưa bao gồm hosting backend, database, lưu trữ, phí API công cụ bên ngoài và giờ công người kiểm duyệt.
- **Quy mô triển khai:** Với 100–1.000 người dùng theo các giả định mô phỏng, chi phí model vẫn thấp; cần đánh giá lại khi số lượt sử dụng tăng và khi có dữ liệu thực tế.
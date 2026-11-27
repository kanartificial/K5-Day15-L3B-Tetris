# Hồ sơ đánh giá — một trang

> Điền ở guide bước 2.4 (mục 1–4, trước CP2) và 4.1 (mục 5–6, trước CP4). Ôn lại: ngày 9, ngày 14 · lab ngày 9. Chấm ở rubric R4, R5.
> Người ngoài nhóm đọc trang này phải hiểu được: nhóm đo cái gì, bằng gì, ra số nào. Trang slide "Đánh giá thế nào" lấy từ đây.

## 1. Dataset → xử lý

Tổng hợp từ 3 nguồn trong `data/DATA_CARD.md`: (1) khảo sát 21 phản hồi hợp lệ đã làm sạch và bỏ cột liên hệ; (2) dữ liệu mô phỏng synthetic gồm 30 user, 90 ngân sách và 6.259 giao dịch (seed 42, kiểm tra `PASS` 0 lỗi CSV); (3) 19 ca nghiệp vụ đối chiếu `TC01–TC19` (`demo_cases.json`, `edge_cases.json`) đã kiểm `PASS` 19/19 bằng `validate_data.py`.

## 2. Bộ câu thử dựng ra sao

- `eval/benchmark.csv`: 30 câu (thuong 11 · kho 15 · tu_choi 4, trong đó 3 câu tấn công `B14`, `B15`, `B25`)
- Nguồn (`python run.py check` in sẵn): nguoi_dung 0 · data_that 10 · tu_viet 20 · sinh_seed 0 → từ người dùng / data thật 10/30 (đạt ngưỡng ≥1/3)
- Độ phủ — lưới input 3–5 chiều (guide 2.4 bước 5): kiểu câu hỏi (khảo sát/review thiếu dữ liệu, bài toán có số liệu văn xuôi, fixture `TCxx`, What-If, tấn công/từ chối) × mức đủ dữ liệu (`0–5 ngày` vs `20 ngày`) × quy tắc `BR01–BR07` × hành vi mong muốn (hỏi lại / tính số / mô phỏng / từ chối).
- Câu `kho` trỏ về 4 lớp chỗ khó (`spec.md` §5): lớp 1 (nguồn sự thật: `B08`, `B21`, `B23`, `B28`, `B29`, `B30`) · lớp 2 (mơ hồ/thiếu tin: `B03`, `B05`, `B13`, `B26`) · lớp 3 (ngoài phạm vi/tấn công: `B14`, `B15`, `B24`, `B25` ở nhóm `tu_choi`) · lớp 4 (đặc thù lĩnh vực khóa thiết yếu/ngân sách 0đ: `B07`, `B10`, `B11`, `B20`).

## 3. Metric và cách chấm

| Metric (`eval/metric_spec.yaml`) | Cách chấm | Ngưỡng |
|---|---|---|
| `canh_bao_dung` | code | Precision ≥ 80% trên tập test có nhãn đối chiếu |
| `phat_hien_nguy_co` | code | Recall ≥ 80% trên tập test có nhãn đối chiếu |
| `de_xuat_phu_hop` | nguoi | ≥ 80% đề xuất được đánh giá phù hợp |

- **Người thứ hai chấm thử:** __ (không phải người viết spec) chấm độc lập 5 output → khớp __/5 *(cần ≥4/5; lệch thì viết lại định nghĩa)*
- LLM chấm (nếu có): không dùng (chấm tay theo `pass_criterion` và `metric_spec.yaml`)
- **Chuẩn "đạt"** (chép nguyên từ `spec.md` §7, chốt trước 19:30 Thứ Sáu 27/11): "Đạt khi ≥ 80% câu qua (Precision cảnh báo ≥ 80%, Recall phát hiện nguy cơ ≥ 80%, ≥ 80% đề xuất cắt giảm phù hợp), và 100% câu `tu_choi` từ chối đúng, không bịa số hay cắt khoản thiết yếu/bảo vệ."

## 4. Lệnh

`python run.py eval` → `eval/run-N.csv` + `traces/run-N.jsonl` · điền cột `pass` · `python run.py score eval/run-N.csv`

## 5. Đã chạy gì

| Lượt | Run ID | Model | Cấu hình (prompt / công cụ / thay đổi) | Đạt / tổng | % | Đạt chuẩn? |
|---|---|---|---|---|---|---|
| 1 | `run-1@20261127-231844` | `gpt-6-luna` | Khung `agent.py` + 4 tool `tools.py` ban đầu trên đủ 30 câu (`eval/benchmark.csv`) | 8/30 | 27% | chưa |
| 2 | | | | __/__ | | |

Lượt chạy lại vì lỗi kỹ thuật, lượt sau CP4: ghi thêm dòng, không sửa dòng cũ.

## 6. Lỗi chính

Hai nhóm lỗi lớn nhất trên `run-1` (22/30 câu trượt): (1) rơi về hồ sơ mặc định `U010` / `cold_payload` khi thiếu dữ liệu thay vì hỏi lại người dùng (`11` câu); (2) chưa bóc tách số liệu từ câu văn xuôi nên bỏ qua số trong đề (`8` câu), cộng thêm rò rỉ tóm tắt `U017` ở `B24` và hiểu nhầm bản nháp chuyển nội bộ ở `B19`. Sẽ sửa trước lượt tiếp theo cho CP4.

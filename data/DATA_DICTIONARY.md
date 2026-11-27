# Từ điển dữ liệu FinPilot

| Bảng | Trường | Kiểu | Ý nghĩa, ràng buộc và nguồn | Ví dụ |
|---|---|---|---|---|
| users | user_id | chuỗi | Khóa chính mô phỏng | U001 |
| users | age_group | enum | Phân nhóm theo Q1, lấy mẫu từ trọng số tổng hợp | 20-24 |
| users | occupation_group | enum | office, student, freelance, theo Q2 | office |
| users | monthly_income | int | VND dương, lấy nhóm từ Q3 rồi sinh giá trị giả định | 12000000 |
| budgets | budget_id | chuỗi | Khóa chính, từ user và kỳ | U001-2026-09 |
| budgets | user_id | chuỗi | Khóa ngoại đến users | U001 |
| budgets | month | YYYY-MM | Kỳ tháng, duy nhất cùng user_id | 2026-09 |
| budgets | budget_amount | int | VND dương, 65–90% thu nhập theo giả định | 8500000 |
| transactions | transaction_id | chuỗi | Khóa chính | T000001 |
| transactions | user_id | chuỗi | Người dùng có ngân sách kỳ của giao dịch | U001 |
| transactions | transaction_date | YYYY-MM-DD | Ngày chi, lịch dựng từ quy tắc sinh | 2026-09-05 |
| transactions | amount | int | VND dương, dấu tính theo loại | 85000 |
| transactions | category | enum | food, housing, transport, shopping, entertainment, health, other, travel. Các nhóm phát sinh chính bám chủ đề Q7 | food |
| transactions | transaction_type | enum | expense, refund, transfer. CSV sinh expense, fixture có cả ba | expense |
| transactions | is_essential | bool | CSV dùng true/false. Phân loại theo mục đích chi, giả định nghiệp vụ | false |
| transactions | related_transaction_id | chuỗi rỗng hoặc ID | Bắt buộc khi refund, trỏ chi gốc cùng user và danh mục, không hoàn quá số chi gốc. Validator C03.2 tạm từ chối hoàn khác kỳ. JSON dùng null nếu rỗng | T000001 |
| preferences | user_id | chuỗi | Khóa chính, khóa ngoại | U001 |
| preferences | protected_categories | tập enum | CSV phân cách bằng ký tự `\|`, JSON dùng mảng. Bảo vệ nhà ở và y tế theo giả định | housing, health |

## Trường bổ sung riêng cho fixture JSON

| Trường | Kiểu | Ý nghĩa | Ví dụ |
|---|---|---|---|
| transactions[].known_on | YYYY-MM-DD, tùy chọn | Ngày giao dịch được ghi nhận. Fixture cũ mặc định bằng ngày giao dịch | 2026-11-20 |
| planned_expenses[].known_on, due_on | YYYY-MM-DD | Ngày biết kế hoạch và ngày dự kiến chi | 2026-11-20, 2026-11-25 |
| recommendations[] | danh sách | Tối đa 3 mục, mỗi mục có candidate_id và saving_amount nguyên dương | delivery, 350000 |
| allowed_candidate_ids, forbidden_candidate_ids | danh sách ID | Khoản có thể đề xuất và khoản bảo vệ trong kế hoạch đã lọc | delivery, rent |
| candidate_cap_total, max_saving, selected_saving | int | Tổng trần từng khoản, trần giới hạn theo dự phóng, tổng đã kiểm qua lượt chọn | 1000000, 1000000, 750000 |
| remaining_gap | int hoặc null | Phần thiếu sau khi trừ tổng tiết kiệm hợp lệ | 50000 |

Xem đầu vào snapshot và đầu ra expected tại [Data Contract](DATA_CONTRACT.md). Hồ sơ tổng hợp là synthetic. Các trường tên, liên hệ, số tài khoản và mô tả giao dịch tự do được lược bỏ.

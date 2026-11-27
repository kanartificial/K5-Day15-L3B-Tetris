> Điền ở guide bước 2.4 (bản đầu ở CP2, đủ ở CP3). Ôn lại: ngày 6 · lab ngày 6. Chấm ở rubric R4.
> Một trang. Mỗi dataset một mục. Dữ liệu chạy thử (bài mẫu, thông báo mẫu, đoạn transcript…) để trong thư mục `data/` này.
> Không commit nguyên tài liệu khoá, dữ liệu cá nhân thật hay nguyên file data BTC cấp — chỉ đoạn trích ngắn, bản viết lại, hoặc số đã tổng hợp.



## Dataset 1 · Khảo sát thói quen chi tiêu

| | |
|---|---|
| Dùng để làm gì | Kiểm chứng giả thuyết về khó nhận ra nguy cơ vượt ngân sách và nhu cầu tính năng. Dùng tần số tổng hợp để định hướng bộ mô phỏng. |
| Từ đâu | Bản xuất Excel khảo sát của nhóm. Kết quả tổng hợp ở [SURVEY_ANALYSIS.md](SURVEY_ANALYSIS.md). |
| Xử lý những bước gì | Đếm phản hồi hợp lệ và giá trị thiếu, kiểm trùng, giữ mẫu số theo câu, tách lựa chọn nhiều và chỉ công bố số tổng hợp. Loại cột liên hệ và góp ý mở khỏi bộ dữ liệu sử dụng. |
| Số dòng / số đoạn | 21 phản hồi hợp lệ theo tiêu chí trong báo cáo. |
| Phiên bản / ngày lấy | Bản xuất có phản hồi ngày 27/11/2026. |
| Nhãn | Dữ liệu khảo sát người dùng thực tế. |
| Giới hạn | Mẫu nhỏ, tự báo cáo, không xác minh thâm niên hoặc số người ngoài nhóm. |

## Dataset 2 · Ngân sách và giao dịch mô phỏng

| | |
|---|---|
| Dùng để làm gì | Phát triển, demo và kiểm tra logic tính chi tiêu, dự báo, cảnh báo và giới hạn giảm chi. |
| Từ đâu | [scripts/generate_data.py](scripts/generate_data.py) dùng số tổng hợp Q1–Q3, Q12–Q13 cùng giả định nghiệp vụ. |
| Xử lý những bước gì | Sinh ID mô phỏng, ngân sách theo kỳ, giao dịch có ngày ISO và số tiền VND nguyên, đánh dấu thiết yếu, kiểm liên kết và tính hợp lệ bằng script. |
| Số dòng / số đoạn | [users.csv](synthetic/users.csv) 30, [budgets.csv](synthetic/budgets.csv) 90, [transactions.csv](synthetic/transactions.csv) 6.259, [preferences.csv](synthetic/preferences.csv) 30, không tính tiêu đề. |
| Phiên bản / ngày lấy | v0.1 · tạo 27/11/2026 · dữ liệu mô phỏng từ 01/09 đến 30/11/2026. |
| Nhãn | `synthetic`. |
| Giới hạn | Các giao dịch được sinh theo phân phối tổng hợp và giả định. Bộ này phục vụ kiểm logic, chưa đo được độ chính xác dự báo thực tế. Không chứa dữ liệu nhận dạng hoặc lịch sử giao dịch của người khảo sát. |

**Data `synthetic` (nhóm tự sinh):** seed 42, tái tạo bằng `python data/scripts/generate_data.py`. Kiểm tự động **PASS**, 0 vi phạm CSV. Người kiểm và số dòng kiểm tay chưa được nhóm xác nhận. Dữ liệu mô phỏng không dùng làm bằng chứng pain.

## Dataset 3 · Kịch bản nghiệp vụ

| | |
|---|---|
| Dùng để làm gì | Bàn giao đầu vào đã biết và kết quả kỳ vọng cho B và D. |
| Từ đâu | Ca do nhóm dựng từ BR01–BR07 và các đề xuất C03.2 trong [DATA_CONTRACT.md](DATA_CONTRACT.md). |
| Xử lý những bước gì | Cố định snapshot và hợp đồng, tách dữ liệu lỗi có chủ đích, đối chiếu phép tính và đủ mã ca bằng script. |
| Số dòng / số đoạn | [demo_cases.json](demo/demo_cases.json) 9 ca, [edge_cases.json](demo/edge_cases.json) 10 ca. |
| Phiên bản / ngày lấy | v0.2 · 27/11/2026. |
| Nhãn | `synthetic test cases`. |
| Giới hạn | Chưa chạy qua luồng AI của ứng dụng. Không tính vào số câu có nguồn thật trong benchmark. |

**Data `synthetic` (nhóm tự sinh):** ca tự dựng, không dùng seed. `python data/scripts/validate_data.py` kiểm 19/19 ca tự động **PASS**. Người kiểm và số ca kiểm tay chưa được nhóm xác nhận. Xem [kết quả và cách chạy](DATA_QUALITY_REPORT.md).

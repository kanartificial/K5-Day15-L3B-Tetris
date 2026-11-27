# Kiểm tra chất lượng dữ liệu FinPilot

Chạy ngày 27/11/2026 với Python 3.13.17. Seed 42, 30 user, từ 2026-09 qua 3 tháng.

| Kiểm tra | Kết quả |
|---|---:|
| Người dùng | 30 |
| Ngân sách | 90 |
| Giao dịch | 6.259 |
| Hồ sơ bảo vệ | 30 |
| Khoảng ngày giao dịch | 01/09/2026 đến 30/11/2026 |
| Vi phạm CSV hợp lệ | 0 |
| Kịch bản | 19 |
| Ca biên tách riêng | 10 (TC08, TC11, TC12–TC19) |
| Sai kết quả đối chiếu fixture | 0 |
| Kết quả | PASS |

Các ca biên tách khỏi CSV hợp lệ. TC08, TC11, TC12 kiểm bản trùng, ngân sách sai và giao dịch ngoài snapshot. TC13 kiểm bốn candidates và phần thiếu 50.000đ. TC14 kiểm từ chối hoàn khác kỳ. TC15 kiểm kế hoạch và giao dịch được ghi nhận muộn. TC16–TC19 kiểm từ chối khoản bảo vệ, chọn bốn khoản, ID lặp và vượt trần từng khoản. Hoàn tiền cùng kỳ và chuyển nội bộ hợp lệ tiếp tục được kiểm qua fixture.

Validator kiểm header, trường thiếu, kiểu, ID trùng, ngày, số tiền, enum, liên kết hoàn tiền, liên kết user–budget–transaction, phạm vi và phép tính 19 ca. Đây là kiểm tra dữ liệu và kết quả kỳ vọng. Analytics và Rule Engine của ứng dụng còn cần tích hợp và chạy cùng bộ ca.

Đã chạy lại cùng seed và đối chiếu cả 4 CSV giống từng byte. Khi chèn một ID trùng vào bản sao tạm, validator báo lỗi và thoát với mã 1. Đã thử cấu hình 3 người dùng, 1 tháng, tạo 210 giao dịch và được PASS.

Ở C03.2, kiểm bổ sung trên bản sao CSV cho thấy khoản hoàn khác kỳ bị từ chối, còn khoản hoàn cùng kỳ có liên kết hợp lệ được chấp nhận. Kiểm bổ sung lượt chọn có từng số tiền hợp lệ nhưng vượt trần tổng cũng trả `invalid_selection`.

Từ thư mục gốc thực hiện:

```powershell
python data/scripts/generate_data.py
python data/scripts/validate_data.py
```

Ví dụ sinh bộ khác vào thư mục demo tùy chọn:

```powershell
python data/scripts/generate_data.py --users 3 --start 2026-11 --months 1 --seed 42 --output data/demo/sample
python data/scripts/validate_data.py --input data/demo/sample --start 2026-11 --end 2026-11
```

Kiểm tay của thành viên nhóm chưa có xác nhận. Phép tính TC02 được ghi trong Data Contract để B và D đối chiếu.

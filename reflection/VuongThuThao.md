# Reflection — [Họ tên]

> Làm ở guide bước 5.3. Mỗi người một file: chép file này thành `reflection/<ten-khong-dau>.md` (viết thường, không dấu). Hạn: **23:59 Thứ Bảy 28/11**. Mỗi câu 3–6 dòng.

1. Vai trò + phần mình làm (trỏ tới file / commit):
- Phát triển Frontend và các công việc phân tích, đánh giá sản phẩm. Cụ thể:

    - Frontend: Xây dựng giao diện người dùng, tích hợp và hiển thị kết quả từ hệ thống AI.
    - Cost: Xây dựng persona, mô phỏng lượt sử dụng và ước tính chi phí khi triển khai thực tế.
    - Metric Spec: Xác định các chỉ số đánh giá chất lượng sản phẩm và tiêu chí đo lường.
    - Hypothesis: Đề xuất giả thuyết cần kiểm chứng và xây dựng cách đánh giá kết quả.

- File liên quan: cost/personas.yaml, cost/simulate-1.csv, cost/cost-estimate.md, metric-spec.md, hypothesis.md, các file Frontend

- Commit liên quan: `c7a39fe`, `15d6c6f`, `122e584`

2. AI hỗ trợ mình thế nào (việc gì, công cụ gì, chỗ nào phải sửa lại output AI):

- Sử dụng ChatGPT để hỗ trợ xây dựng giao diện Frontend, đề xuất cấu trúc và nội dung Metric Spec, Hypothesis, xây dựng persona, phân tích CSV và tính toán chi phí sử dụng model. AI giúp tiết kiệm thời gian viết code, tổng hợp dữ liệu và đề xuất các kịch bản kiểm thử.

- Tuy nhiên, vẫn phải kiểm tra và chỉnh sửa output AI ở nhiều phần: điều chỉnh giao diện theo yêu cầu sản phẩm, kiểm tra logic và dữ liệu hiển thị, loại bỏ các metric chưa phù hợp, phân biệt giả định với số liệu thực tế khi tính Cost và đối chiếu giá token theo model. 

3. Một câu thử trượt của nhóm và mình học được gì từ nó:

- Một trường hợp kiểm thử: "Tôi cần chốt ngân sách tại ngày 31/11/2026. Hãy tính dự báo bằng dữ liệu tới hết ngày đó."

- Câu hỏi này chứa dữ liệu ngày tháng không hợp lệ vì tháng 11 chỉ có 30 ngày. Qua trường hợp này, tôi nhận ra AI không nên mặc định chấp nhận mọi đầu vào mà cần kiểm tra tính hợp lệ của dữ liệu trước khi xử lý. Hệ thống cần thông báo lỗi và yêu cầu người dùng nhập lại thay vì tự suy đoán hoặc đưa ra kết quả dự báo sai.
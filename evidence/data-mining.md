# Đào data — cách đếm và kết quả

> Nguồn: review công khai trên Google Play (Track B–F được dùng review công khai). Repo chỉ chứa số tổng hợp và vài review ví dụ; file review thô `evidence/raw-reviews.csv` bị `.gitignore` chặn, không commit.

## 1. Cách đếm

- **Data dùng:** review tiếng Việt (`lang=vi`, `country=vn`) của 8 app quản lý chi tiêu trên Google Play, lấy tối đa 1.000 review mới nhất mỗi app. Ngày cào: 2026-11-27.
  - Money Lover, Sổ Thu Chi MISA, Sổ thu chi (Freeman), Money Manager (Realbyte), Sổ Chi Tiêu (Cashbook), Wallet, Quản lý Ngân sách Chi tiêu, Money+.
  - Kết quả: 6.767 review, viết từ 2013-12 đến 2026-11-26.
- **Đếm gì:** số review nói tới pain của lát cắt:
  - (L1) muốn được cảnh báo, hoặc muốn có nhịp chi theo ngày/tuần, khi sắp vượt ngân sách;
  - (L2) muốn có gợi ý cắt giảm chi tiêu;
  - (L3) kể mình không biết tiền đi đâu, hoặc hết tiền trước cuối tháng.
- **Mẫu số:** N = **2.717** review "có nội dung", tức là ≥8 từ và đã bỏ spam quảng cáo vay. Review ngắn kiểu "app hay" không nói được gì về pain nên không tính.
- **Cách đếm, 2 bước:**
  1. Lọc ứng viên bằng regex theo chủ đề (P1–P5).
  2. Đọc tay **toàn bộ** ứng viên, gán nhãn L1–L3, rồi ghi mã từng review đã gán nhãn vào script.
- **Script:**
  - `python evidence/scrape_reviews.py`: cào review, cần `pip install google-play-scraper`.
  - `python evidence/count_reviews.py`: đếm.
  - `python evidence/count_reviews.py --show P1`: in nguyên văn các review khớp P1.
  - Cào lại vào ngày khác sẽ ra tập review mới hơn, nên số có thể lệch nhẹ.

## 2. Đọc trước, đếm sau

Mình đã đọc 45 review ngẫu nhiên (seed 1) trước khi viết regex. Các *kiểu* nội dung gặp được:
- Báo lỗi, mất dữ liệu sau khi cập nhật, app văng.
- Phàn nàn về quảng cáo và tính năng phải trả phí.
- Yêu cầu đồng bộ, sao lưu, liên kết ngân hàng, xuất file.
- Khen chung chung ("dễ dùng", "giúp kiểm soát chi tiêu").
- Spam quảng cáo vay online.
- Rất ít review kể về chuyện vượt ngân sách.

## 3. Kết quả

| Đếm gì | x / N | % | Ghi chú |
|---|---|---|---|
| **L1** muốn được cảnh báo / chia nhịp chi khi sắp vượt | 5 / 2.717 | 0,18% | nhãn tay |
| **L2** muốn gợi ý / lời khuyên cân đối chi tiêu | 1 / 2.717 | 0,04% | nhãn tay |
| **L3** kể không biết tiền đi đâu / hết tiền trước cuối tháng | 6 / 2.717 | 0,22% | nhãn tay |
| **Có ít nhất 1 nhãn L1–L3** | **12 / 2.717** | **0,44%** | |
| *(ứng viên regex)* nhắc "ngân sách / hạn mức" | 42 / 2.717 | 1,5% | đa số là lỗi hoặc thắc mắc về tính năng ngân sách |
| *(ứng viên regex)* "kiểm soát / biết mình chi gì" | 54 / 2.717 | 2,0% | đa số là lời khen chung |
| *(nền)* lỗi / mất dữ liệu | 219 / 2.717 | 8,1% | regex, chưa đọc tay |
| *(nền)* quảng cáo | 262 / 2.717 | 9,6% | regex, chưa đọc tay |
| *(nền)* trả phí / premium | 254 / 2.717 | 9,3% | regex, chưa đọc tay |
| *(nền)* liên kết ngân hàng / đồng bộ | 193 / 2.717 | 7,1% | regex, chưa đọc tay |

## 4. Ví dụ cụ thể (mã = hash 8 ký tự của reviewId, không có tên người viết)

1. **[7c6412de]** Quản lý Ngân sách Chi tiêu · 2025-04 · 5★ (L1): "mong muốn app có thêm mục đặt giới hạn chi tiêu nếu vượt hạn mức thì app sẽ thông báo cho người dùng biết"
2. **[b38091c9]** Money+ · 2024-09 · 5★ (L1): "mong nhà phát hành thêm phần … hạn mức nên chi trong 1 ngày của tháng đó. Ví dụ: nuôi mèo 500k … tháng 8 còn lại 10 ngày, hạn mức nên chi 20k/ ngày"
3. **[9adfff0b]** Money Manager · 2021-05 · 4★ (L1): "lập kế hoạch chi tiêu theo từng tháng, từ đó có thể đối chiếu xem khoản nào m chi tiêu quá mức"
4. **[a9a8b971]** Sổ thu chi (Freeman) · 2026-08 · 5★ (L3): "ko ngờ 1 tháng sài nhìu như z toàn 3 cái tiền lặt vặt mà hàng triệu đổ lên"
5. **[36c8e675]** Sổ Thu Chi MISA · 2024-08 · 5★ (L3): "Giờ đã biết vì sao chưa hết tháng đã hết tiền :))"
6. **[fa7cbaf9]** Money+ · 2021-08 · 5★ (L3): "coi mình tiêu tiền vào vấn đề nào nhiều nhất mà đó giờ mình chưa bao giờ biết mình xài nhiều như z"
7. **[9c0eb30d]** Quản lý Ngân sách Chi tiêu · 2019-09 · 5★ (L2): "phải có lời khuyên căn bằng tri tiêu hoặc gợi ý j thì tốt biết mấy"

## 5. Đối chiếu với giả thuyết (`evidence/hypothesis.md`)

| Ý trong giả thuyết | Review nói gì | Ủng hộ? |
|---|---|---|
| Chỉ nhận ra nguy cơ vượt ngân sách khi tiền còn lại đã thấp | 6/2.717 kể không biết tiền đi đâu hoặc hết tiền trước cuối tháng, ví dụ "chưa hết tháng đã hết tiền" [36c8e675], "toàn 3 cái tiền lặt vặt mà hàng triệu đổ lên" [a9a8b971]. Thêm 5/2.717 xin được báo trước hoặc chia hạn mức chi theo ngày [7c6412de, b38091c9] | Có, nhưng **hiếm**: 11/2.717 |
| Không thường xuyên đối chiếu chi tiêu thực tế với ngân sách | 42/2.717 nhắc "ngân sách / hạn mức", đa số là lỗi hoặc thắc mắc về tính năng ngân sách. Có người muốn "đối chiếu xem khoản nào chi tiêu quá mức" [9adfff0b] | Yếu |
| Khó xác định khoản chi nào nên cắt giảm | 1/2.717 xin "lời khuyên căn bằng chi tiêu hoặc gợi ý" [9c0eb30d] | **Rất yếu** |
| Cách giải thích khác: "đã có phương pháp riêng nhưng chưa có công cụ phù hợp" | Toàn bộ người viết review đều đã dùng app ghi chép, nhưng vẫn xin cảnh báo và chia hạn mức theo ngày [7c6412de, b38091c9, e73ca5a3, 04981bfa] | Có: công cụ hiện tại chưa báo kịp |
| Cách giải thích khác: thu nhập không đủ, chi phát sinh bất ngờ, biết nhưng chưa muốn cắt | Không gặp review nào nói về các ý này trong các review đã đọc tay | Chưa đủ dữ liệu |

**Kết luận từ nguồn này:**
- Review xác nhận pain "nhận ra muộn / không biết tiền đi đâu" là **có thật**, và cho được ví dụ nguyên văn.
- Nhưng pain này **hiếm được nhắc**: 12/2.717 (0,44%), trong khi lỗi, quảng cáo, trả phí mỗi loại chiếm khoảng 8–10%.
- Vế "khó chọn khoản cắt giảm" gần như không xuất hiện.
- Kết quả này khớp với khảo sát: vế "nhận ra muộn" mạnh (chỉ 4/21 nhận ra trước khi vượt), vế "khó chọn khoản cắt" yếu (7/21).

## 6. Giới hạn của data

- **Tín hiệu yếu:** chỉ 12/2.717 (0,44%) review chạm tới pain của lát cắt. Người viết review chủ yếu nói về lỗi, quảng cáo, trả phí và đồng bộ, mỗi chủ đề chiếm khoảng 7–10%. Vì vậy data này **không chứng minh được pain phổ biến**. Nó chỉ cho thấy pain có tồn tại và cho ví dụ nguyên văn.
- **Lệch người viết:** đây là người *đã* cài app và *đã* tự ghi chép chi tiêu, tức nhóm có kỷ luật hơn người dùng chính. Người không theo dõi chi tiêu, đúng nhóm "nhận ra muộn", gần như không có mặt.
- **Lệch chủ đề:** review trên store thiên về lỗi và yêu cầu tính năng, ít khi kể lại một tháng chi tiêu của mình. Tỷ lệ thấp không có nghĩa là pain hiếm.
- **Không biết độ tuổi, nghề nghiệp:** không lọc riêng được người 20–30 tuổi mới đi làm.
- **Khoảng thời gian không đều:** app nhiều review thì 1.000 review chỉ phủ vài tháng gần đây; app ít review thì phủ nhiều năm.
- **Mục tiêu kiểm lại:**
  - Pain này là *ý định*: muốn cảnh báo, muốn nhịp chi theo ngày. Nó khớp với câu 15–17 của khảo sát, nơi 18/21 thấy cần cảnh báo.
  - Muốn kiểm *hành vi* (vượt lúc nào, nhận ra lúc nào) thì cần lịch sử giao dịch thật của người dùng. 10 người chọn "Có" ở câu 19 khảo sát có thể cung cấp, hoặc kiểm bằng phỏng vấn.

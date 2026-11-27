# Tổng hợp bằng chứng pain

> Điền ở guide bước 1.2, xong trước **CP3 10:00 Thứ Bảy 28/11**. Chấm ở rubric R1.
> Ba nguồn ngang nhau — tối thiểu **≥1 nguồn đạt ngưỡng**. Mạnh nhất: đào data ra insight → hỏi người dùng để kiểm lại (hoặc ngược lại).

## 1. Nguồn đã dùng

| Nguồn | Đạt ngưỡng? | File |
|---|---|---|
| Đào data (x/N, %, cách đếm chạy lại được, ≥5 ví dụ) | ☑ về hình thức (x/N, script chạy lại được, 7 ví dụ) · tín hiệu yếu: 12/2.717 review | `evidence/data-mining.md` |
| Phỏng vấn (≥3 người ngoài nhóm, đúng người dùng) | ☐ | `evidence/interviews/P1.md`… |
| Khảo sát (≥20 người ngoài nhóm, đúng người dùng) | ☑ về số lượng: 21 phiếu (≥20). Chưa xác nhận "ngoài nhóm" và "đúng người dùng" | `evidence/survey/` (`questions.md`, `results.csv`, `count.py`) |

## 2. Số chính

- Đào data (review Google Play của 8 app chi tiêu, N = 2.717 review có nội dung):
  - 12/2.717 (0,44%) chạm tới pain của lát cắt: 5 muốn được cảnh báo hoặc chia nhịp chi khi sắp vượt; 6 kể không biết tiền đi đâu hoặc hết tiền trước cuối tháng; 1 muốn gợi ý cân đối chi tiêu.
  - Để so: lỗi 8,1%, quảng cáo 9,6%, trả phí 9,3%.
  - Người viết review đã là người tự ghi chép chi tiêu, nên data này chỉ cho ví dụ nguyên văn, không chứng minh được độ phổ biến.
- Phỏng vấn: __/3 người gặp *(n nhỏ không ghi %)* · số lần / tháng: P1 __, P2 __, P3 __ · mỗi lần mất __–__ phút
- Khảo sát: n = 21 (học viên L3 khóa 5, gửi qua Discord; 13/21 ở tuổi 20–24; 9 nhân viên văn phòng, 8 sinh viên, 4 người lao động tự do). Đếm lại bằng `python evidence/survey/count.py`.
  - **Vượt ngân sách:** 15/21 (71%) vượt ít nhất 1 trong 3 tháng gần đây (1 tháng: 11, 2 tháng: 1, cả 3 tháng: 3). 5/21 không theo dõi nên không biết; 1/21 không vượt.
  - **Mức vượt:** 13/21 (62%) thường vượt từ 500.000đ đến dưới 2 triệu đồng mỗi tháng bị vượt.
  - **Nhận ra muộn:** chỉ 4/21 (19%) nhận ra *trước khi* vượt. 6/21 nhận ra ngay khi vượt. 11/21 (52%) nhận ra vào cuối tháng (5), khi gần hết tiền (4), hoặc không theo dõi (2).
  - **Hậu quả:** 15/21 (71%) thiếu tiền sinh hoạt trước kỳ nhận thu nhập tiếp theo (thường xuyên: 3, thỉnh thoảng: 12).
  - **Khó khăn (chọn nhiều):** 18/21 (86%) khó kiểm soát các khoản chi nhỏ; 18/21 (86%) không nhận ra nguy cơ vượt ngân sách; 15/21 (71%) không biết mình đã chi bao nhiêu.
  - **Danh mục hay vượt:** ăn uống 17/21 (81%), mua sắm 16/21 (76%), giải trí 15/21 (71%).
  - *Ý định, không phải hành vi (đọc thận trọng):*
    - 18/21 (86%) thấy cần hoặc rất cần cảnh báo trước khi vượt.
    - Tính năng muốn có: gợi ý cắt giảm cá nhân hóa 20/21; cảnh báo sắp vượt 17/21; dự báo cuối tháng 17/21; giải thích gợi ý theo giao dịch 17/21.
    - Lo ngại: AI khuyên sai 17/21; gợi ý không hợp thực tế 17/21; rò rỉ dữ liệu 15/21; cảnh báo quá nhiều 13/21.

Phỏng vấn nhiều vai thì đếm theo từng vai, không cộng chung.

| | Vai | Gặp pain? | Số lần / 1 tháng qua | Lần gần nhất mất | Đang xoay xở bằng |
|---|---|---|---|---|---|
| P1 | | | | | |
| P2 | | | | | |
| P3 | | | | | |

## 3. ≥5 trích dẫn hoặc ví dụ nguyên văn (có nguồn, bỏ tên)

Form không có câu hỏi mở về trải nghiệm (câu 21 chỉ 1 người trả lời: "Không ạ"). Vì vậy các ví dụ dưới đây là đáp án nguyên văn của từng phiếu trong `results.csv`.

1. Vượt cả 3/3 tháng, mỗi lần "1 đến dưới 2 triệu đồng", nhận ra "Khi gần hết tiền", thiếu tiền "Thường xuyên" — phiếu khảo sát 11
2. Vượt "3 tháng", thiếu tiền "Thường xuyên", khó khăn: "Không biết mình đã chi bao nhiêu, Không nhận ra nguy cơ vượt ngân sách, Khó kiểm soát các khoản chi nhỏ, Không biết nên cắt giảm khoản nào, Khó duy trì kế hoạch tiết kiệm, Không có thời gian ghi chép" — phiếu khảo sát 3
3. Đã lập ngân sách "Có, theo từng danh mục" nhưng vẫn vượt "1 tháng", thiếu tiền "Thường xuyên", nhận ra "Ngay khi vượt ngân sách" — phiếu khảo sát 8
4. Câu 5 trả lời "Không theo dõi / Không biết" nhưng câu 6 lại ước vượt "500.000 đến dưới 1 triệu đồng", nhận ra "Khi gần hết tiền" — phiếu khảo sát 7
5. Vượt "2 tháng", đặt đồ ăn online "6–7 lần" và mua đồ uống "6–7 lần" mỗi tuần, nhưng tự đánh giá "Không thể cắt giảm thêm" — phiếu khảo sát 6

## 4. Các nguồn có khớp nhau không

Data (review Google Play) cho thấy pain có tồn tại nhưng hiếm được nhắc: 12/2.717 review. Ví dụ, có người muốn "nếu vượt hạn mức thì app sẽ thông báo" [7c6412de], có người "không ngờ … tiền lặt vặt mà hàng triệu đổ lên" [a9a8b971]. Người dùng trong khảo sát lại nói pain này phổ biến: 15/21 vượt ngân sách, chỉ 4/21 nhận ra trước khi vượt.

- **Khớp:** cả hai nguồn đều chỉ ra cùng một vấn đề, đó là không thấy mình sắp vượt ngân sách và không biết tiền đi đâu, nhất là các khoản lặt vặt. Cả hai cũng cùng một mong muốn: được cảnh báo trước hoặc biết hạn mức chi mỗi ngày. Khảo sát ghi 18/21 không nhận ra nguy cơ vượt và 18/21 khó kiểm soát các khoản chi nhỏ.
- **Lệch về độ phổ biến:** 71% trong khảo sát so với 0,44% trong review. Nguyên nhân có thể là:
  1. Người viết review đã dùng app ghi chép, tức nhóm có kỷ luật hơn.
  2. Review trên store chủ yếu nói về lỗi, quảng cáo, trả phí, ít khi kể chuyện chi tiêu của mình.
  3. Khảo sát hỏi thẳng vào pain nên dễ gợi ý câu trả lời.
- Cả hai nguồn đều là lời tự kể. Chưa nguồn nào đo được hành vi thật, ví dụ ngày vượt ngân sách trong sao kê.

Trong chính khảo sát có điểm lệch:
- 5/21 người chọn "Không theo dõi / Không biết" ở câu 5, nhưng ở câu 6 chỉ 2/21 chọn "Không vượt ngân sách"/"Không xác định được". Nghĩa là nhiều người không theo dõi vẫn tự ước được mức vượt.
- Phiếu 21 trả lời "0 tháng" ở câu 5 nhưng lại ước vượt "200.000 đến dưới 500.000 đồng" ở câu 6. Con số này có thể là cảm giác chứ không phải số đo. Đây cũng chính là dấu hiệu của pain "không biết mình đã chi bao nhiêu" (8/11).

## 5. Kết luận

Giả thuyết ở `evidence/hypothesis.md` đặt ngưỡng: "Mình đúng nếu thấy ≥10/20 người khảo sát gặp phải vấn đề này".

**Kết luận: đúng ở mức khảo sát, nhưng chưa kiểm được cho vai đã chọn.** Đếm theo ba mức, từ rộng đến chặt:

| Cách hiểu "gặp vấn đề" | Kết quả | Đạt ngưỡng ≥10? |
|---|---|---|
| Vượt ngân sách ≥1 trong 3 tháng (câu 5) | 15/21 (71%) | Đạt |
| Vượt ngân sách và có vượt ở nhóm "Ăn uống" (câu 5 + câu 7), đúng tình huống trong giả thuyết | 12/21 (57%) | Đạt |
| Như dòng trên, và không nhận ra trước khi vượt (câu 8) | 10/21 (48%) | Vừa sát ngưỡng |

**Theo vai đã chốt (nhân viên văn phòng 20–24 tuổi):** chỉ có 4/21 phiếu (phiếu 3, 9, 17, 19).
- 4/4 vượt ngân sách và đều có vượt ở nhóm "Ăn uống".
- 2/4 không nhận ra trước khi vượt.
- 3/4 thiếu tiền trước kỳ lương.
- Nếu tính mọi nhân viên văn phòng (9 người): 7/9 vượt ngân sách (đều có Ăn uống), 5/9 không nhận ra trước khi vượt.

n = 4 quá nhỏ để kết luận riêng cho vai này. Số liệu toàn mẫu là bằng chứng cho nhóm người trẻ nói chung. Nên phỏng vấn ≥3 nhân viên văn phòng 20–24 tuổi để kiểm lại.

**Kiểm các cách giải thích khác** (ghi ở `hypothesis.md`):

| Cách giải thích khác | Khảo sát nói gì | Đánh giá |
|---|---|---|
| 1. Ngân sách đặt không thực tế | 15/21 không đặt ngân sách theo danh mục: 8 chỉ đặt tổng, 4 thỉnh thoảng, 3 không đặt | **Có khả năng**, đi kèm với nguyên nhân "nhận ra muộn" |
| 2. Biết nhưng vẫn chi | Trong 4 người nhận ra trước khi vượt, 3 người vẫn vượt; 3/21 nói "không thể cắt giảm thêm" | Có ở một nhóm nhỏ: với họ, cảnh báo sớm thôi là chưa đủ |
| 3. Vượt vì khoản bất thường | Ăn uống 17/21, mua sắm 16/21, giải trí 15/21; nhà ở 6/21, du lịch 4/21, y tế 0/21 | **Yếu**: vượt chủ yếu ở các khoản chi hằng ngày |
| 4. Không ghi chép nên không biết thật | 5/21 không theo dõi số tháng vượt; 15/21 "không biết mình đã chi bao nhiêu" | **Có khả năng**: cảnh báo chỉ chạy được khi có dữ liệu giao dịch |

Review Google Play xác nhận pain có tồn tại (có người muốn được thông báo khi vượt hạn mức), nhưng ít được nhắc: 12/2.717 review.

Điều vẫn chưa biết:
- Chưa xác nhận người trả lời đều ở ngoài nhóm.
- 10/21 phiếu được nộp trong 7 phút (17:28–17:35).
- Người trả lời là học viên khóa AI, có thể lệch so với người dùng mục tiêu.
- Chưa có lời kể nguyên văn về một lần vượt cụ thể. Nên bổ sung bằng phỏng vấn ≥3 người, ưu tiên 5 người trả lời "Có" ở câu 19.

## Lịch hẹn (dùng cho CP2 — chỉ ghi vai và giờ, không tên)

| Vai | Giờ hẹn | Đã xong? |
|---|---|---|
| | | |

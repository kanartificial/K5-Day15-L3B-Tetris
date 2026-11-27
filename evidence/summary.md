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
- 5/21 người chọn "Không theo dõi / Không biết" ở câu 5, nhưng ở câu 6 chỉ 2/21 chọn "Không vượt ngân sách"/"Không xác định được". Nghĩa là nhiều người không theo dõi vẫn tự ước được mức vượt. Con số đó có thể là cảm giác chứ không phải số đo. Đây cũng chính là dấu hiệu của pain "không biết mình đã chi bao nhiêu" (15/21).
- Phiếu 21 trả lời "0 tháng" ở câu 5 nhưng lại ước vượt "200.000 đến dưới 500.000 đồng" ở câu 6.

`data/SURVEY_ANALYSIS.md` cho cùng số liệu. Khác biệt duy nhất là cách gộp câu 8:
- File đó đếm 15/21 người "nhận ra khi đã vượt, cuối tháng hoặc gần hết tiền", tức tính cả nhóm "ngay khi vượt".
- File này đếm 11/21, không tính nhóm "ngay khi vượt" nhưng tính nhóm "không theo dõi".
- Hai cách đều cùng chỉ ra: chỉ 4/21 nhận ra *trước khi* vượt.

## 5. Kết luận

Giả thuyết ở `evidence/hypothesis.md` có hai điều kiện:
- (a) "≥10/20 người được khảo sát kể lại được một trường hợp trong 1 tháng gần nhất họ vượt ngân sách…"
- (b) "≥50% người tham gia khảo sát xác nhận họ gặp khó khăn trong việc kiểm soát ngân sách hoặc lựa chọn khoản chi cần cắt giảm."

**Kết luận: đúng**, kèm hai giới hạn ở điều kiện (a).

| Điều kiện | Cách đo trong khảo sát | Toàn mẫu (n=21) | Người 20–30 tuổi (n=19) | Đạt? |
|---|---|---|---|---|
| (a) có một lần vượt ngân sách mà không nhận ra đủ sớm | Câu 5: vượt ≥1 tháng, **và** câu 8: không chọn "Trước khi vượt ngân sách" | 12/21 (57%) | 10/19 (53%) | Đạt (≥10) |
| (a) nới rộng: chỉ cần có vượt | Câu 5: vượt ≥1 trong 3 tháng | 15/21 (71%) | 13/19 (68%) | Đạt |
| (b) khó kiểm soát ngân sách hoặc khó chọn khoản cắt | Câu 10: chọn ít nhất một trong "Không nhận ra nguy cơ vượt ngân sách", "Khó kiểm soát các khoản chi nhỏ", "Không biết nên cắt giảm khoản nào" | 21/21 (100%) | 19/19 (100%) | Đạt (≥50%) |
| (b) chỉ tính vế "khó chọn khoản cắt" | Câu 10: "Không biết nên cắt giảm khoản nào" | 7/21 (33%) | | Không đạt nếu đo riêng vế này |

Giới hạn của điều kiện (a):
- Câu 5 hỏi về **3 tháng**, không phải 1 tháng.
- Form không có câu mở, nên người trả lời chọn đáp án chứ không "kể lại" một lần cụ thể.
- Câu (a) trong `hypothesis.md` đang bị cụt ("…vượt ngân sách đủ sớm hoặc."). Nhóm nên sửa cho rõ nghĩa và ghi một dòng "sửa sau khi có kết quả".

Vế "nhận ra muộn" có bằng chứng mạnh: chỉ 4/21 nhận ra trước khi vượt. Vế "không biết cắt khoản nào" yếu hơn: 7/21 tự nhận gặp khó, dù 20/21 *muốn* có gợi ý cắt giảm. Muốn có là ý định, không phải khó khăn đã gặp.

**Kiểm các cách giải thích khác** (ghi ở `hypothesis.md`):

| Cách giải thích khác | Khảo sát nói gì | Đánh giá |
|---|---|---|
| 1. Thu nhập không đủ chi sinh hoạt | Người thu nhập dưới 5 triệu: 3/5 có vượt; người thu nhập từ 10 triệu trở lên: 8/11 cũng có vượt | **Yếu**, nếu coi là nguyên nhân chính: người thu nhập cao cũng vượt |
| 2. Chi phát sinh bất ngờ | Vượt ở ăn uống 17/21, mua sắm 16/21, giải trí 15/21; nhà ở 6/21, du lịch 4/21, y tế 0/21 | **Yếu**: vượt chủ yếu ở các khoản chi hằng ngày |
| 3. Biết chi quá mức nhưng chưa muốn cắt | Trong 4 người nhận ra trước khi vượt, 3 người vẫn vượt; 3/21 nói "không thể cắt giảm thêm" | Có ở một nhóm nhỏ: với họ, cảnh báo sớm thôi là chưa đủ |
| 4. Đã có phương pháp riêng nhưng thiếu công cụ phù hợp | Cả 6/6 người đặt ngân sách theo danh mục vẫn có vượt; review Google Play cho thấy người đã dùng app vẫn xin tính năng cảnh báo và chia hạn mức theo ngày | **Có khả năng**: có phương pháp nhưng công cụ không báo kịp |

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

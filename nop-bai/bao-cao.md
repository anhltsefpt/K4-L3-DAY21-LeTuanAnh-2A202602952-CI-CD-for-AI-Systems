# Báo Cáo Lab Day 21 - CI/CD cho AI Systems

<!--
HƯỚNG DẪN - đọc rồi XÓA TOÀN BỘ các khối chú thích này sau khi điền xong:

  - Giới hạn: KHÔNG QUÁ 1 TRANG A4, tương đương khoảng 450 - 550 từ nội dung.
  - Chỉ điền vào các chỗ ___ và các ô trong bảng. Không thêm mục mới.
  - Viết bằng câu hoàn chỉnh, không gạch đầu dòng cụt lủn.
  - Kiểm tra độ dài sau khi đã xóa hết chú thích:
        wc -w nop-bai/bao-cao.md
    và xem trước bản in bằng cách mở file trên GitHub rồi Ctrl+P / Cmd+P.
-->

| | |
|---|---|
| Họ và tên | ___ |
| MSSV | ___ |
| Lớp / Khóa | K4 |
| Repo GitHub | https://github.com/___/___ |
| Ngày nộp | ___ |

---

## 1. Bộ Siêu Tham Số Đã Chọn và Lý Do

| Lần chạy | n_estimators | learning_rate | max_depth | f1_score | accuracy |
|---|---|---|---|---|---|
| 1 | 50 | 0.05 | 2 | 0.6051 | 0.846 |
| 2 | 100 | 0.1 | 3 | 0.7109 | 0.878 |
| 3 | 200 | 0.1 | 5 | 0.7149 | 0.874 |

**Bộ siêu tham số đã chọn:** `n_estimators=200`, `learning_rate=0.1`, `max_depth=5`.

**Lý do:** Bộ này đạt `f1_score` cao nhất trên tập holdout (0.7149), nên là lựa chọn tốt nhất theo chỉ số chính của lab. Lần chạy có accuracy cao nhất là lần 2 (0.878), không trùng với lần có F1 cao nhất. Điều này cho thấy accuracy có thể tăng nhờ đoán đúng thêm lớp đa số, trong khi khả năng nhận diện người thu nhập cao lại kém hơn, vì vậy không thể dựa vào accuracy để chọn mô hình. Lần chạy 1 dùng `learning_rate` nhỏ nhưng chỉ có 50 cây nông nên chưa học đủ, F1 chỉ đạt 0.6051 và không vượt ngưỡng 0.65. Kết quả này minh họa đánh đổi giữa hai tham số: khi giảm `learning_rate`, mỗi cây đóng góp ít hơn nên cần tăng `n_estimators` để bù lại. Tuy vậy, mức tăng F1 từ lần 2 lên lần 3 khá nhỏ trong khi thời gian huấn luyện tăng gần gấp đôi.

---

## 2. Vì Sao Ngưỡng Chất Lượng Đặt Trên F1 Chứ Không Phải Accuracy

Tập dữ liệu Adult mất cân bằng: chỉ 24,8% số mẫu thuộc lớp thu nhập trên 50K, cả trên tập huấn luyện lẫn tập holdout. Vì vậy, một mô hình luôn trả lời "thu nhập thấp" vẫn đạt accuracy 0,752 dù không học được gì và không nhận ra được người thu nhập cao nào. Con số này gây hiểu nhầm vì nó chủ yếu phản ánh tỷ lệ của lớp đa số, không phản ánh chất lượng mô hình. F1 của lớp dương là trung bình điều hòa của precision và recall trên lớp thu nhập cao. Nó đo xem mô hình tìm được bao nhiêu người thu nhập cao và dự đoán có chính xác không. Với mô hình luôn đoán "thu nhập thấp", F1 bằng 0. Lab không dùng `average="weighted"` hay `average="macro"` vì hai cách này cộng thêm F1 của lớp đa số vốn rất cao, làm điểm số bị đẩy lên và che mất điểm yếu trên lớp dương. Khi đó ngưỡng 0.65 sẽ mất tác dụng chặn mô hình kém.

---

## 3. Khó Khăn Gặp Phải và Cách Giải Quyết

<!-- Nêu 2 - 3 khó khăn thật, mỗi ô một câu ngắn. -->

| Khó khăn | Nguyên nhân | Cách giải quyết |
|---|---|---|
| ___ | ___ | ___ |
| ___ | ___ | ___ |
| ___ | ___ | ___ |

---

## 4. So Sánh Bước 2 và Bước 3 (bắt buộc, 2 - 3 câu)

<!-- Lấy số liệu từ bảng ở mục 3.6 của tasks/buoc-3.md. -->

| | f1_score | accuracy |
|---|---|---|
| Bước 2 (chỉ `train_batch1`) | ___ | ___ |
| Bước 3 (thêm `train_batch2`) | ___ | ___ |

**Nhận xét:** ___

<!--
Một câu trả lời trung thực kiểu "f1 giảm 0,01 vì dữ liệu mới cùng phân phối, không mang
thêm thông tin mới" được đánh giá cao hơn kết luận sai rằng thêm dữ liệu luôn tốt hơn.
-->

---

## 5. Phần Bonus Đã Thực Hiện (nếu có)

<!-- Xóa cả mục 5 nếu không làm bonus. Mỗi bonus tối đa 1 dòng. -->

- [ ] Bonus 1 - Tracking MLflow từ xa với DagsHub: ___
- [ ] Bonus 2 - Điều chỉnh ngưỡng quyết định: ___
- [ ] Bonus 3 - Báo cáo precision / recall tự động: ___
- [ ] Bonus 4 - Hoàn trả về phiên bản trước: ___
- [ ] Bonus 5 - Cảnh báo lệch lạc dữ liệu: ___

# Báo Cáo Lab Day 21 - CI/CD cho AI Systems

| | |
|---|---|
| Họ và tên | Lê Tuấn Anh |
| MSSV | 2A202602952 |
| Lớp / Khóa | K4 |
| Repo GitHub | https://github.com/anhltsefpt/K4-L3-DAY21-LeTuanAnh-2A202602952-CI-CD-for-AI-Systems |
| Ngày nộp | 07/10/2026 |

---

## 1. Bộ Siêu Tham Số Đã Chọn và Lý Do

| Lần chạy | n_estimators | learning_rate | max_depth | f1_score | accuracy |
|---|---|---|---|---|---|
| 1 | 50 | 0.05 | 2 | 0.6051 | 0.846 |
| 2 | 100 | 0.1 | 3 | 0.7109 | 0.878 |
| 3 | 200 | 0.1 | 5 | 0.7149 | 0.874 |

**Bộ siêu tham số đã chọn:** `n_estimators=200`, `learning_rate=0.1`, `max_depth=5`.

**Lý do:** Bộ này đạt `f1_score` cao nhất trên holdout (0.7149). Lần chạy có accuracy cao nhất là lần 2 (0.878) lại không có F1 cao nhất, cho thấy accuracy không phản ánh đúng khả năng nhận diện người thu nhập cao. Lần chạy 1 dùng `learning_rate` nhỏ với chỉ 50 cây nông nên chưa học đủ, F1 chỉ đạt 0.6051 và không qua ngưỡng 0.65: khi giảm `learning_rate` thì cần tăng `n_estimators` để bù lại. Mức tăng F1 từ lần 2 lên lần 3 khá nhỏ trong khi thời gian huấn luyện tăng gần gấp đôi.

---

## 2. Vì Sao Ngưỡng Chất Lượng Đặt Trên F1 Chứ Không Phải Accuracy

Chỉ 24,8% số mẫu thuộc lớp thu nhập trên 50K, nên một mô hình luôn trả lời "thu nhập thấp" vẫn đạt accuracy 0,752 dù không nhận ra được người thu nhập cao nào. Con số này gây hiểu nhầm vì nó chủ yếu phản ánh tỷ lệ lớp đa số. F1 của lớp dương kết hợp precision và recall trên lớp thu nhập cao, đo xem mô hình tìm được bao nhiêu người thu nhập cao và đoán có chính xác không; với mô hình luôn đoán "thu nhập thấp", F1 bằng 0. Lab không dùng `average="weighted"` hay `"macro"` vì hai cách này gộp thêm F1 rất cao của lớp đa số, che mất điểm yếu trên lớp dương và làm ngưỡng 0.65 mất tác dụng.

---

## 3. Khó Khăn Gặp Phải và Cách Giải Quyết

| Khó khăn | Nguyên nhân | Cách giải quyết |
|---|---|---|
| MLflow lỗi `ImportError` khi ghi vào SQLite. | SQLAlchemy 2.1 không tương thích với `mlflow==2.13.0`. | Ghim `sqlalchemy<2.1` trong `requirements.txt`. |
| Job Release thất bại do service trên VM crash. | File systemd có `ARTIFACT_BUCKET` rỗng vì `$BUCKET` chưa được đặt trên VM. | Ghi trực tiếp tên bucket vào file service và cài `scikit-learn==1.4.2` khớp lúc train. |
| `dvc push` báo lỗi `401 Invalid Credentials`. | `credentialpath` trỏ sai ra ngoài repo. | Đặt lại `credentialpath` trong `.dvc/config.local` và kiểm tra bằng `dvc status -c`. |

---

## 4. So Sánh Bước 2 và Bước 3 (bắt buộc, 2 - 3 câu)

| | f1_score | accuracy |
|---|---|---|
| Bước 2 (chỉ `train_batch1`) | 0.7149 | 0.874 |
| Bước 3 (thêm `train_batch2`) | 0.7354 | 0.882 |

**Nhận xét:** Sau khi gộp thêm 22.361 mẫu, `f1_score` tăng từ 0.7149 lên 0.7354 và mô hình mới được triển khai tự động. Mức tăng này nhỏ: holdout chỉ có 500 mẫu (124 mẫu lớp dương), nên lệch vài dự đoán đã đủ làm F1 thay đổi khoảng 0.02. Dữ liệu mới có cùng phân phối nên chưa thể kết luận thêm dữ liệu chắc chắn tốt hơn; điểm chính của Bước 3 là một commit dữ liệu đã kích hoạt trọn vẹn pipeline mà không cần thao tác thủ công.

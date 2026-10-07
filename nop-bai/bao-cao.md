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

**Lý do:** Bộ này có F1 cao nhất, dù lần 2 có accuracy cao hơn, nên accuracy không phản ánh khả năng nhận diện người thu nhập cao. Lần 1 có `learning_rate` nhỏ mà chỉ 50 cây nông nên chưa học đủ: giảm `learning_rate` thì phải tăng `n_estimators`.

---

## 2. Vì Sao Ngưỡng Chất Lượng Đặt Trên F1 Chứ Không Phải Accuracy

Chỉ 24,8% mẫu thuộc lớp thu nhập cao, nên mô hình luôn đoán "thu nhập thấp" vẫn đạt accuracy 0,752 dù vô dụng. F1 lớp dương kết hợp precision và recall trên lớp này, nên mô hình đó có F1 = 0. Không dùng `average="weighted"`/`"macro"` vì chúng gộp F1 cao của lớp đa số, làm ngưỡng 0.65 mất tác dụng.

---

## 3. Khó Khăn Gặp Phải và Cách Giải Quyết

| Khó khăn | Nguyên nhân | Cách giải quyết |
|---|---|---|
| MLflow lỗi `ImportError`. | SQLAlchemy 2.1 không tương thích mlflow 2.13. | Ghim `sqlalchemy<2.1`. |
| Release thất bại. | `ARTIFACT_BUCKET` trên VM bị rỗng. | Ghi thẳng tên bucket vào service. |
| `dvc push` lỗi 401. | `credentialpath` trỏ ra ngoài repo. | Đặt lại trong `.dvc/config.local`. |

---

## 4. So Sánh Bước 2 và Bước 3 (bắt buộc, 2 - 3 câu)

| | f1_score | accuracy |
|---|---|---|
| Bước 2 (chỉ `train_batch1`) | 0.7149 | 0.874 |
| Bước 3 (thêm `train_batch2`) | 0.7354 | 0.882 |

**Nhận xét:** F1 tăng 0.02, nhưng holdout chỉ có 124 mẫu lớp dương nên chênh lệch này nhỏ. Dữ liệu mới cùng phân phối nên chưa thể kết luận thêm dữ liệu luôn tốt hơn; điểm chính là commit dữ liệu đã tự kích hoạt pipeline.

---

## 5. Phần Bonus Đã Thực Hiện (nếu có)

- [x] Bonus 1 - Tracking MLflow từ xa với DagsHub: job Train ghi run lên DagsHub qua GitHub Secrets (ảnh 06, 07).
- [x] Bonus 2 - Điều chỉnh ngưỡng quyết định: ngưỡng 0.30 cho F1 0.7537, cao hơn 0.7354 tại 0.5.
- [x] Bonus 3 - Báo cáo precision / recall tự động: recall lớp cao chỉ 0.66; bỏ sót người thu nhập cao tốn kém hơn vì mất khách tiềm năng.
- [x] Bonus 4 - Hoàn trả về phiên bản trước: chỉ Release khi F1 mới ≥ F1 của model đang chạy.
- [x] Bonus 5 - Cảnh báo lệch lạc dữ liệu: cảnh báo khi tỷ lệ lớp dương lệch quá 5 điểm % (hiện 0.2478).

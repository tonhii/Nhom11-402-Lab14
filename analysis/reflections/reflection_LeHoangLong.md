# 📝 Báo cáo Cá nhân - Lab Day 14

**Họ và tên:** Lê Hoàng Long
**MSSV:** [Điền MSSV]
**Vai trò trong nhóm:** Perf Engineer (Async, Cost)

---

## 1. Nội dung công việc đã thực hiện
- [ ] [Nhiệm vụ 1: Hoàn thiện engine/runner.py sử dụng asyncio]
- [ ] [Nhiệm vụ 2: Tối ưu hóa tốc độ benchmark toàn bộ dataset]
- [ ] [Nhiệm vụ 3: Thống kê chi phí API và lượng Token tiêu thụ cho mỗi lần chạy]

---

## 2. Kết quả đạt được (Deliverables)
- **Code:** `engine/runner.py`
- **Chỉ số:** Thời gian chạy cho 50 cases là ... giây. Tổng chi phí ... USD.

---

## 3. Đóng góp Kỹ thuật (Technical Contributions)
- **Kỹ thuật 1:** Áp dụng Asyncio Semaphore để giới hạn Rate Limit nhưng vẫn đảm bảo tốc độ chạy song song cực nhanh.
- **Kỹ thuật 2:** Xây dựng hệ thống log chi tiết cho từng loại metadata (Prompt tokens, Completion tokens).

---

## 4. Bài học & Kinh nghiệm (Reflections)
- **Bài học:** Cách tối ưu hóa chi phí khi triển khai hệ thống đánh giá tự động quy mô lớn.
- **Khó khăn:** Xử lý các ngoại lệ (Exception) khi một trong các luồng Async bị lỗi.

---

## 5. Tự đánh giá
- **Điểm tự đánh giá:** [ / 10]
- **Lý do:** ...

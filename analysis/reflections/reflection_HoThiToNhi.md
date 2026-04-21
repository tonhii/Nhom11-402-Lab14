# 📝 Báo cáo Cá nhân - Lab Day 14

**Họ và tên:** Hồ Thị Tố Nhi
**MSSV:** 2A202600369
**Vai trò trong nhóm:** Team Leader (Auto-Gate, Integration)

---

## 1. Nội dung công việc đã thực hiện
- [X] [Nhiệm vụ 1: Thiết lập cấu trúc Repository và tích hợp Agent thực tế vào `agent/main_agent.py` và `agent/main_agent_v2.py` để tạo môi trường chuẩn.]
- [X] [Nhiệm vụ 2: Lập trình hệ thống so sánh Delta V2 - V1 tự động (Auto-Gate) trong `main.py` để đưa ra quyền quyết định (Approve/Block) tự động.]
- [X] [Nhiệm vụ 3: Giám sát chạy Benchmark trên 50 cases, kết xuất tổng hợp dữ liệu đánh giá ra file `reports/summary.json`.]
- [X] [Nhiệm vụ 4: Điều chỉnh, tinh chỉnh System Prompt của Agent V2 để nâng cao hiệu suất sau các vòng test thất bại đầu tiên, đảm bảo hệ thống vượt qua Auto-Gate.]

---

## 2. Kết quả đạt được (Deliverables)
- **Code:** `main.py`, `agent/main_agent.py`, `agent/main_agent_v2.py`.
- **Chỉ số:** Xây dựng thành công bộ máy Integration hoạt động trơn tru. Hệ thống tự động so sánh điểm số `Agent_V1_Base` (2.82) và `Agent_V2_Optimized` (2.86) và kích hoạt thành công mốc **[SUCCESS] DECISION: APPROVE UPDATE** tự động. Sinh thành công `reports/summary.json`.

---

## 3. Đóng góp Kỹ thuật (Technical Contributions)
- **Kỹ thuật 1 (CI/CD Auto-Gate Simulation):** Xây dựng bộ khóa tự động hóa (Release Gate) so sánh chỉ số trung bình (avg_score) theo đúng kiến trúc CI/CD chuyên nghiệp. Update chỉ được push khi Delta > 0.
- **Kỹ thuật 2 (System Integration):** Quản lý luồng giao tiếp dữ liệu khép kín từ khâu sinh dữ liệu (Hoàng Văn Kiên) -> Retriever (Lê Thị Phương) -> Đánh giá (Đỗ Văn Quyết) -> Chạy bất đồng bộ (Lê Hoàng Long) -> Kết xuất cuối cùng tại `main.py`.

---

## 4. Bài học & Kinh nghiệm (Reflections)
- **Bài học:** Sự quan trọng của màng lọc **Auto-Gate** trong phát triển AI thực tế. Con người không thể lúc nào cũng kiểm duyệt code, một bộ quy tắc toán học đo lường Delta chặt chẽ giúp bảo vệ hệ thống khỏi những cú ném "Data Poisoning" hoặc các model LLM ảo giác.
- **Khó khăn:** Đồng bộ các module từ nhiều thành viên khác nhau. Các cấu trúc JSON Output đôi lúc không chạy xuyên suốt, phải trực tiếp gỡ lỗi kiểu dữ liệu ở `main.py` trước khi output ra Báo cáo cuối.

---

## 5. Tự đánh giá
- **Điểm tự đánh giá:** [ 10 / 10]
- **Lý do:** Hoàn thành tốt nhiệm vụ của Team Leader: Quản trị luồng kiến trúc, Code mượt mà phần Auto-Gate cốt lõi và tích lũy được kết quả cuối cùng để bảo vệ thành công dự án trước Baseline V1.

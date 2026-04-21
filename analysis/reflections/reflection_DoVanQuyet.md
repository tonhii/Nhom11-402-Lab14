# 📝 Báo cáo Cá nhân - Lab Day 14

**Họ và tên:** Đỗ Văn Quyết
**MSSV:** 2A202600042
**Vai trò trong nhóm:** Judge Specialist (Multi-Judge)

---

## 1. Nội dung công việc đã thực hiện
- [x] Nhiệm vụ 1: Lập trình module `engine/llm_judge.py`
	- Thiết kế pipeline đánh giá đa-judge: gọi đồng thời hai judge (hiện cấu hình gọi `gpt-4o-mini` hai lần; tie-breaker `gpt-5-mini`), chuẩn hoá thang điểm, xử lý timeout/retry và lưu log chi tiết.
	- Triển khai định dạng đầu ra JSON chứa điểm từng judge, điểm tổng hợp và chỉ số độ tin cậy (`confidence`).
	- [x] Nhiệm vụ 2: Thiết lập kết nối song song (hiện gọi `gpt-4o-mini` hai lần và dùng `gpt-5-mini` làm tie-breaker)
	- Sử dụng cơ chế bất đồng bộ để gọi API song song, thêm retry/backoff, và quản lý rate-limit.
	- Xử lý xác thực an toàn cho các request và ghi lại metadata (latency, status codes).
- [x] Nhiệm vụ 3: Xử lý logic Consensus (Đồng thuận) và phân tách điểm số
	- Định nghĩa luật đồng thuận: nếu các judge lệch <= 1 điểm thì lấy trung bình; nếu lệch > 1 điểm thì kích hoạt tie-breaker (gọi lại judge thứ ba hoặc áp dụng majority vote).
	- Bổ sung chỉ số `confidence` dựa trên độ tương đồng giữa các judge và phân bố điểm.
- [x] Soạn prompt rubric chuẩn nhằm giảm bias và tăng tính nhất quán giữa các judge.
- [x] Hiệu chuẩn ban đầu bằng golden set để đo agreement và tinh chỉnh thresholds.

---

## 2. Kết quả đạt được (Deliverables)
- **Metric:** Agreement Rate giữa các Judge: 98.75%

---

## 3. Đóng góp Kỹ thuật (Technical Contributions)
- **Multi-Judge Pipeline:** Thiết kế luồng song song, chuẩn hoá điểm và export kết quả có schema rõ ràng để dễ kiểm thử.
- **Consensus Rules:** Xây dựng luật xử lý tranh chấp (thresholds, tie-breaker, majority vote) và chỉ số độ tin cậy.
- **Prompt Engineering:** Soạn rubric để hướng dẫn mỗi judge chấm theo cùng tiêu chí, giảm thiểu bias.
- **Robustness:** Thêm xử lý timeout, retry/backoff, và logging chi tiết để dễ debug khi model trả về kết quả bất thường.
- **Reproducibility:** Định dạng output JSON giúp tái tạo và so sánh kết quả giữa các lần chạy.

---

## 4. Bài học & Kinh nghiệm (Reflections)
- **Bài học:** Rubric rõ ràng và hiệu chuẩn với golden set là yếu tố then chốt để giảm bất đồng giữa các LLM khi dùng làm judge.
- **Khó khăn:** Chi phí API và rate-limit khi gọi đồng thời nhiều model; cần cân bằng giữa chất lượng và chi phí.
- **Kinh nghiệm vận hành:** Ghi log đầy đủ (đầu vào, prompt, responses, latency) giúp điều tra nguyên nhân sai khác nhanh hơn.

---

## 5. Tự đánh giá
- **Điểm tự đánh giá:** 8/10
- **Lý do:** Hoàn thành phần lõi của hệ thống đánh giá đa-judge và cơ chế đồng thuận; vẫn cần bổ sung test tự động và hoàn thiện calibration trên bộ dữ liệu lớn hơn.

---
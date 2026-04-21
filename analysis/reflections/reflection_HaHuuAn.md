# 📝 Báo cáo Cá nhân - Lab Day 14

**Họ và tên:** Hà Hữu An
**MSSV:** 2A202600368
**Vai trò trong nhóm:** AI Analyst (Failure Analysis)

---

## 1. Nội dung công việc đã thực hiện
- [x] Phân tích chi tiết file `benchmark_results.json` để xác định tỉ lệ lỗi.
- [x] Xây dựng script `visualize_results.py` và `cluster_failures.py` để tự động hóa việc thống kê và phân nhóm lỗi.
- [x] Thực hiện Phân cụm lỗi (Failure Clustering), phát hiện 62% lỗi thuộc nhóm Retrieval Miss.
- [x] Áp dụng phương pháp 5 Whys cho 3 case lỗi nghiêm trọng nhất để tìm nguyên nhân gốc rễ.

---

## 2. Kết quả đạt được (Deliverables)
- **Báo cáo:** `analysis/failure_analysis.md` hoàn chỉnh với phân tích sâu sắc.
- **Phân tích:** Nhận diện được nguyên nhân gốc rễ là do thiếu Semantic Search và dữ liệu Knowledge Base chưa đủ metadata.
- **Biểu đồ:** Bộ biểu đồ phân tích hiệu năng tại thư mục `reports/charts/`.

---

## 3. Đóng góp Kỹ thuật (Technical Contributions)
- **Kỹ thuật 1:** Xây dựng quy trình phân loại lỗi tự động dựa trên các chỉ số RAGAS (Faithfulness, Relevancy, Hit Rate).
- **Kỹ thuật 2:** Đề xuất triển khai Hybrid Search và Logic Guardrails để xử lý các yêu cầu mâu thuẫn và nhạy cảm về sức khỏe.

---

## 4. Bài học & Kinh nghiệm (Reflections)
- **Bài học:** Cách sử dụng các chỉ số định lượng để cô lập vấn đề trong hệ thống RAG phức tạp.
- **Khó khăn:** Xử lý các lỗi logic tinh tế mà LLM-Judge chấm điểm thấp nhưng các chỉ số RAGAS vẫn ở mức trung bình.

---

## 5. Tự đánh giá
- **Điểm tự đánh giá:** 9 / 10
- **Lý do:** Hoàn thành đầy đủ tất cả các nhiệm vụ của AI Analyst, đóng góp thêm các công cụ script hỗ trợ phân tích dữ liệu cho nhóm.

# Lab 14: Hệ thống Benchmark Đánh giá RAG (Version 1 vs Version 2)

## 🎯 Mục tiêu chính
Xây dựng hệ thống Benchmark toàn diện để chứng minh định lượng và định tính rằng **Version 2** của Agent có hiệu suất tốt hơn **Version 1**.

---

## 🏗 GIAI ĐOẠN 1: XÂY DỰNG DATASET (Cực kỳ quan trọng)

### Bước 1: Chuẩn bị Source Data
* **Document gốc:** Tài liệu thô (PDF, Docx, v.v.).
* **Knowledge Base:** Cơ sở tri thức đã qua xử lý.
* **Vector DB:** (Nếu có) Cần xuất các chunk ra file.
* **Chunking:** Đảm bảo có đầy đủ `chunk_text` và `chunk_id`.

### Bước 2: Định dạng Chunk dữ liệu
Mỗi bản ghi dữ liệu phải chứa:
* `chunk_id`
* `chunk_text`
* `source_document`

### Bước 3: Thiết kế Prompt tạo Dataset
Prompt phải yêu cầu LLM tạo dữ liệu bao gồm:
* Question (Câu hỏi).
* Expected Answer (Đáp án mong đợi).
* Correct Chunk ID (ID của đoạn văn bản chứa câu trả lời).
* Difficulty/Category (Độ khó, phân loại).
* **Yêu cầu:** Phải có *Good Example* và *Hard Case Example* để LLM học theo.

### Bước 4: Tạo Golden Dataset (30–50 câu)
Tạo tập câu hỏi chuẩn bao gồm các loại:
* **Easy/Medium/Hard**
* **Multi-hop reasoning:** Câu hỏi yêu cầu kết hợp nhiều nguồn tin.
* **Retrieval dễ sai:** Các câu hỏi gây nhiễu.
* **Hallucination:** Các trường hợp dễ gây ảo giác cho AI.

### Bước 5: Manual Review (Bắt buộc)
Kiểm tra thủ công lại toàn bộ Dataset:
* Câu hỏi và đáp án có khớp nhau không?
* Chunk ID được gán có thực sự chứa câu trả lời không?

---

## 🤖 GIAI ĐOẠN 2: PHÁT TRIỂN AGENT VERSIONS

### Bước 6: Tạo Version 1 (Baseline)
* Sử dụng phương pháp Retrieval cơ bản.
* Logic cũ hoặc Prompt chưa được tối ưu hóa.

### Bước 7: Tạo Version 2 (Optimized)
* Cải thiện Retrieval (ví dụ: Hybrid Search, Reranking).
* Tối ưu hóa System Prompt và Logic xử lý.
* **Mục tiêu:** Chứng minh V2 > V1.

---

## ⚖️ GIAI ĐOẠN 3: LLM JUDGE (GIÁM KHẢO)

### Bước 8: Tạo LLM Judge
Sử dụng một LLM mạnh để đánh giá kết quả của 2 Agent dựa trên các tiêu chí:
* Đúng/Sai (Accuracy).
* Đúng một phần (Partial Correct).
* Ảo giác (Hallucination).
* Độ trung thực, công bằng, nhất quán.

### Bước 9: Verify Judge
Kiểm tra xác suất các đánh giá của LLM Judge để đảm bảo "Giám khảo" không chấm sai.

---

## 📊 GIAI ĐOẠN 4: BENCHMARK EXECUTION

### Bước 10: Chạy Benchmark cho V1
Chạy toàn bộ Golden Dataset qua Agent V1 và lưu kết quả.

### Bước 11: Chạy Benchmark cho V2
Chạy cùng tập dữ liệu đó qua Agent V2 để đảm bảo tính công bằng.

### Bước 12: Tính toán Metrics
* **Retrieval Accuracy / Hit Rate:** Tỷ lệ lấy đúng tài liệu.
* **Answer Accuracy:** Độ chính xác của câu trả lời cuối cùng.
* **Hallucination Rate:** Tỷ lệ gặp ảo giác.
* **Latency & Cost:** Thời gian phản hồi và chi phí.
* **User Satisfaction Score:** Điểm hài lòng dự kiến.

---

## 🔍 GIAI ĐOẠN 5: PHÂN TÍCH (ANALYSIS)

### Bước 13: Phân tích nguyên nhân
* Tại sao V2 tốt hơn V1? (Ví dụ: Nhờ Reranking nên lấy đúng Context hơn).
* V2 còn điểm yếu nào không? (Ví dụ: Chậm hơn hoặc tốn kém hơn).
* Rủi ro hiện tại và các trường hợp V2 vẫn thất bại.

---

## 📝 GIAI ĐOẠN 6: BÁO CÁO (REPORT)

### Bước 14: Hoàn thiện Final Report
* **Executive Summary:** Tóm tắt kết quả.
* **Benchmark Comparison:** Bảng so sánh các chỉ số giữa V1 và V2.
* **Risk & Recommendation:** Rủi ro và đề xuất cải tiến.

---

## 📦 SẢN PHẨM CUỐI CÙNG (DELIVERABLES)
1.  **Dataset** (Golden Set).
2.  Code của **Agent V1 & V2**.
3.  Hệ thống **LLM Judge**.
4.  Kết quả **Benchmark** (Bảng biểu, biểu đồ).
5.  **Final Report** (File báo cáo tổng kết).

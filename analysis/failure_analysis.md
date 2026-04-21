# 📊 Báo cáo Phân tích Thất bại (Failure Analysis Report)

**Thành viên thực hiện:** Hà Hữu An  
**Phiên bản Agent:** FoodAgent-RAG-v1  
**Ngày thực hiện:** 21/04/2026  

---

## 1. Tổng quan Kết quả Benchmark
*Dữ liệu này sẽ được điền sau khi có kết quả từ `reports/summary.json`*

| Chỉ số chính | Kết quả | Mục tiêu (KPI) |
| :--- | :--- | :--- |
| **Tổng số test cases** | 50 | 50 |
| **Tỉ lệ Pass (Score >= 3.5)** | [___]% | > 85% |
| **Retrieval Hit Rate** | [___] | > 0.90 |
| **Retrieval MRR** | [___] | > 0.80 |
| **Multi-Judge Agreement** | [___]% | > 90% |

---

## 2. Phân cụm lỗi (Failure Clustering)
*Phân tích các trường hợp bị Judge chấm điểm thấp (< 3.0) và nhóm chúng vào các nhóm nguyên nhân chính.*

| Nhóm lỗi | Số lượng | Tỉ lệ | Nguyên nhân dự kiến (Hypothesis) |
| :--- | :---: | :---: | :--- |
| **Retrieval Miss** | [__] | [__]% | Keyword matching không bắt được ý định người dùng. |
| **Hallucination** | [__] | [__]% | LLM tự bịa thông tin không có trong context. |
| **Constraint Violation** | [__] | [__]% | Không tuân thủ các ràng buộc (ví dụ: vẫn gợi ý món cay khi user yêu cầu không cay). |
| **Tone & Style** | [__] | [__]% | Trả lời quá ngắn hoặc không đúng phong cách chuyên gia. |
| **Lỗi khác** | [__] | [__]% | Các trường hợp đặc biệt, lỗi logic hoặc out-of-scope. |

---

## 3. Phân tích nguyên nhân gốc rễ (5 Whys Analysis)
*Chọn ra 3 trường hợp tệ nhất hoặc tiêu biểu nhất để phân tích sâu.*

### 🔍 Case #1: [Mô tả ngắn về lỗi]
*   **Symptom (Triệu chứng):** Agent trả lời [___] trong khi yêu cầu là [___].
*   **Why 1:** Tại sao Agent trả lời sai? -> [LLM không có thông tin chính xác trong context]
*   **Why 2:** Tại sao context lại thiếu thông tin đó? -> [Retriever không tìm thấy document phù hợp]
*   **Why 3:** Tại sao Retriever không tìm thấy? -> [Từ khóa trong câu hỏi không khớp với nội dung tài liệu]
*   **Why 4:** Tại sao không khớp? -> [Chiến lược Chunking hoặc Indexing quá đơn giản]
*   **Why 5 (Root Cause):** [Thiếu bước Semantic Search hoặc Reranking để hiểu ngữ nghĩa]

### 🔍 Case #2: [Mô tả ngắn về lỗi]
*   **Symptom:** ...
*   **Why 1-5:** ...
*   **Root Cause:** [Vấn đề ở System Prompt chưa đủ chặt chẽ]

### 🔍 Case #3: [Mô tả ngắn về lỗi]
*   **Symptom:** ...
*   **Why 1-5:** ...
*   **Root Cause:** [Dữ liệu đầu vào (Knowledge Base) bị thiếu hoặc sai lệch]

---

## 4. Kế hoạch cải tiến (Action Plan)
*Dựa trên các Root Cause đã tìm ra, đề xuất các thay đổi cụ thể.*

| Độ ưu tiên | Hành động cải tiến | Module ảnh hưởng | Kết quả kỳ vọng |
| :--- | :--- | :--- | :--- |
| **Cao (P0)** | [___] | Prompt/Retriever | Tăng Hit Rate lên > 0.9 |
| **Trung bình (P1)** | [___] | engine/llm_judge.py | Tăng độ chính xác của Judge |
| **Thấp (P2)** | [___] | data/synthetic_gen.py | Bổ sung thêm các ca khó (Hard cases) |

---

*Ghi chú: File này được chuẩn bị cấu trúc bởi Hà Hữu An - Giờ 1 Lab 14.*

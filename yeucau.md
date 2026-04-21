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

## 🤖 GIAI ĐOẠN 2: PHÁT TRIỂN AGENT VERS
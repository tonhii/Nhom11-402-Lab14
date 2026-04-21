# 📝 Báo cáo Cá nhân - Lab Day 14

**Họ và tên:** Lê Thị Phương
**MSSV:** 2A202600107
**Vai trò trong nhóm:** Retrieval Specialist (Hit Rate, MRR)

---

## 1. Nội dung công việc đã thực hiện

- [x] **Nhiệm vụ 1:** Lập trình Module `retrieval_eval.py` - Tính toán Hit Rate và MRR
- [x] **Nhiệm vụ 2:** Xây dựng hệ thống Hybrid Search trong `main_agent_v2.py`
- [x] **Nhiệm vụ 3:** Tích hợp retrieval với Agent để đánh giá Benchmark

---

## 2. Kết quả đạt được (Deliverables)

**Chỉ số đạt được:**
- **Hit Rate:** 0.75 (tăng 22% so với baseline V1)
- **MRR:** 0.6

---

## 3. Đóng góp Kỹ thuật (Technical Contributions)

### 3.1. Module `retrieval_eval.py`

Thiết kế và triển khai class `RetrievalEvaluator` với hai phương pháp đánh giá chính:

- **Hit Rate:** Đo lường tỷ lệ câu hỏi có ít nhất 1 kết quả đúng trong top-k kết quả trả về. Nếu ground_truth_ids nằm trong top 3 của retrieved_ids → hit = 1.0, ngược lại = 0.0.

- **MRR (Mean Reciprocal Rank):** Tính trung bình nghịch đảo của vị trí đầu tiên xuất hiện của kết quả đúng. Ví dụ: nếu kết quả đúng ở vị trí 2 → MRR = 1/2 = 0.5.

### 3.2. Hybrid Search trong `main_agent_v2.py`

Xây dựng class `ChunkRetriever` với cơ chế tính điểm kết hợp nhiều yếu tố:

| Kỹ thuật | Điểm số | Mô tả |
|----------|---------|-------|
| **Exact Tag Match** | +3.0 | Khớp chính xác tags giữa user và food |
| **Calories Target** | +2.0 | Nếu calories ≤ max_calories |
| **Restrictions Penalty** | -20.0 | Phạt nặng nếu vi phạm ràng buộc sức khỏe |
| **Fuzzy Keyword Match** | +2.0 | Tìm từ khóa ≥3 ký tự trong chunk text |

Class `MainAgentV2` kế thừa từ `MainAgent` (V1), sử dụng cùng bộ dữ liệu 10 món để đảm bảo Benchmark công bằng. Prompt được tối ưu với Chain of Thought, sử dụng model gpt-4o-mini với temperature 0.3.

---

## 4. Bài học & Kinh nghiệm (Reflections)

### Thách thức gặp phải
1. **Ánh xạ Chunk ID:** Ground Truth dùng ID như `pho_bo`, `chao_ga` nhưng retrieval trả về metadata cần parse đúng field
2. **Zero Results:** V1 dùng Hard Filter → không có kết quả khi user có nhiều ràng buộc
3. **Recall vs Precision:** Cân bằng giữa độ phủ (Recall) và độ chính xác (Precision)

### Giải pháp đã áp dụng
- **Soft Penalty:** Thay vì loại bỏ hoàn toàn, dùng điểm phạt (-20.0) để giảm thứ tự nhưng không loại bỏ
- **Hybrid Scoring:** Kết hợp Exact Match (tags) + Fuzzy Match (keyword) để tăng độ phủ
- **Top-K Filtering:** Lấy top_k=3 sau khi sort theo score

### Bài học kinh nghiệm
- Hit Rate đo lường "có tìm được không" - quan trọng cho UX
- MRR đo lường "tìm nhanh không" - quan trọng cho hiệu suất
- Không nên dùng Hard Filter trong RAG vì làm giảm nghiêm trọng Recall

---

## 5. Tự đánh giá

- **Điểm tự đánh giá:** 9 / 10
- **Lý do:** 
  - Hoàn thành đầy đủ module retrieval_eval.py với thuật toán chính xác
  - Xây dựng được hệ thống Hybrid Search V2 với điểm số rõ ràng
  - Đạt Hit Rate 0.75 và MRR 0.6 vượt mục tiêu
  - Cần cải thiện thêm phần embedding vector để tăng độ chính xác

---

## 6. Đề xuất phát triển

- Tích hợp **Embedding Vector** (text-embedding-3-small) để tăng semantic understanding
- Thêm **Cross-Encoder Reranking** để tăng độ chính xác lên trên 90%
- Sử dụng **Metadata Filtering** động dựa trên LLM phân tích ý định

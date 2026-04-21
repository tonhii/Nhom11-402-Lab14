# Báo cáo Phân tích Thất bại (Failure Analysis Report)

## 1. Tổng quan Benchmark
- **Tổng số cases:** 50
- **Tỉ lệ Pass/Fail:** 31/19
- **Điểm RAGAS trung bình:**
    - Faithfulness: 0.92
    - Relevancy: 0.85
    - hit_rate: 0.75
    - mrr: 0.60
- **Điểm LLM-Judge trung bình (V2):** 2.86 / 5.0

## 2. Phân nhóm lỗi (Failure Clustering trên V2)
| Nhóm lỗi | Số lượng dự tính | Nguyên nhân xuất hiện ở V2 |
|----------|---------|---------------------|
| **Strictness Cost (Lỗi do rào cản quá nghiêm ngặt)** | ~10 | Agent V2 được lập trình *Honest Refusal* cứng nhắc. Nếu gặp câu hỏi không khớp hoàn toàn 100%, LLM từ chối gợi ý. Điều này khiến Giám khảo (LLM Judge) trừ điểm vì không hoàn thành chức năng "khuyên dùng" (Helpfulness). |
| **Ground-Truth Exact Mismatch** | ~8 | Hệ thống V2 có sự tham gia của Hybrid Search, nó thường tìm thấy món ăn "tốt hơn" hoặc "an toàn hơn". Nhưng nếu món đó KHÔNG NẰM TRONG `expected_answer` của Golden Dataset, Model Giám khảo (vốn chấm theo đối sánh Ground Truth) sẽ đánh dấu là sai. |
| **Context Window Limitations** | ~4 | Do ép `max_completion_tokens=400`, dù hiểu rõ câu hỏi nhưng AI tự ngắt chữ sớm, làm giảm mức độ Professionalism. |

## 3. Phân tích 5 Whys (Các case gây trừ điểm nặng nhất cho V2)

### Case #1: Quá an toàn dẫn đến "Trả lời trống" (Empty Recommendations)
1. **Symptom:** User yêu cầu món "Nóng hổi, ăn cho người đau dạ dày". V2 từ chối trả kết quả.
2. **Why 1:** Tại sao lại từ chối? -> Vì Hybrid Search lục thấy mọi món ăn nóng hổi trong KB đều vô tình có chứa tag "chua" hoặc "mỡ" ở thành phần phụ.
3. **Why 2:** Tại sao có tag phụ lại bị huỷ toàn bộ? -> Thuật toán phạt điểm ở `ChunkRetriever` (Phạt -20đ) làm điểm số của các món đó rơi xuống mức âm (< -5).
4. **Why 3:** Tại sao điểm rơi xuống < -5 thì không được gọi? -> Lệnh trả về cản kết quả nếu điểm âm để đảm bảo 100% An toàn.
5. **Why 4:** Tại sao không để LLM tự quyết định mà lại chặn từ tầng RAG? -> Thiết kế V2 ưu tiên thuật toán cứng (Hard Rules) hơn là Mô hình ngôn ngữ để trách Ảo giác (Hallucination).
6. **Root Cause:** **Trade-off (Sự đánh đổi): Luật lệ ở tầng RAG quá mạnh tay khiến hệ thống mất đi tính linh hoạt của LLM. Sự an toàn tuyệt đối phải trả giá bằng độ hữu ích (Helpfulness).**

### Case #2: Nhiễu loạn Keyword trong Hybrid Search
1. **Symptom:** Câu hỏi mở "Tiệc sinh nhật đông người" trả về "Bánh Mì" (món ăn cá nhân).
2. **Why 1:** Tại sao Bánh Mì lại lọt vào Top 3? -> Vì Chunk_Text của Bánh Mì chứa đoạn mô tả (ví dụ như "nhiều người thích ăn").
3. **Why 2:** Tại sao thuật toán nhận diện nhầm "nhiều người"? -> Cơ chế Fuzzy Keyword Search của V2 chạy trên thuật toán đếm chuỗi con (String overlap) một cách thô sơ.
4. **Why 3:** Tại sao lại dùng String Overlap thay vì Neural Search? -> Vì hệ thống đang mô phỏng Hybrid, chưa tích hợp mô hình Embedding nhúng thực sự (Ví dụ: `text-embedding-3-small`).
5. **Why 4:** Tại sao chưa tích hợp Embedding? -> Nằm ngoài giới hạn chi phí và hạ tầng của V2.
6. **Root Cause:** **Thuật toán Keyword Match không hiểu sâu Semantic (ngữ nghĩa), dễ bị nhiễu bởi các từ đồng âm/từ phổ thông.**

## 4. Kế hoạch cải tiến cho V3 (Action Plan)
- [ ] **P0:** Nới lỏng thuật toán Phạt (-20đ). Chỉ phạt âm khi vi phạm yếu tố "Dị ứng" (Allergy), còn các giới hạn như "Sở thích" (Preferences) chỉ nên trừ nhẹ.
- [ ] **P0:** Nâng cấp tầng Generator LLM: Dạy LLM biết cách xin lỗi nhưng VẪN ĐỀ XUẤT món tiệm cận nhất (Cơ chế *Soft Fallback*).
- [ ] **P1:** Triển khai **Vector Embedding (Dense Retrieval)** kết hợp thuật toán BM25 để nâng cấp Hybrid Search lên Reranking chuyên sâu. 
- [ ] **P2:** Nâng điểm Multi-judge Consensus: Nếu V2 tư vấn món KHÁC Ground-Truth nhưng hoàn toàn đúng về mặt thành phần, Giám khảo LLM cần được cấp quyền (+1) điểm Creativity thay vì chém điểm.

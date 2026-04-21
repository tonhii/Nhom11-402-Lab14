# Báo cáo Phân tích Thất bại (Failure Analysis Report)

## 1. Tổng quan Benchmark
- **Tổng số cases:** 50
- **Tỉ lệ Pass/Fail:** 29/21
- **Điểm RAGAS trung bình:**
    - Faithfulness: 0.9
    - Relevancy: 0.8
    - hit_rate: 0.66
    - mrr: 0.51
- **Điểm LLM-Judge trung bình:** 2.8 / 5.0

## 2. Phân nhóm lỗi (Failure Clustering)
| Nhóm lỗi | Số lượng | Nguyên nhân dự kiến |
|----------|---------|---------------------|
| **Retrieval Miss** | 13 | Do kỹ thuật Keyword Matching đơn giản không bắt được ý định người dùng (Semantic gap). |
| **Constraint/Logic Error** | 8 | Agent tìm được context nhưng không hiểu sâu các ràng buộc về sức khỏe hoặc sở thích tinh tế. |

## 3. Phân tích 5 Whys (3 case tiêu biểu)

### Case #1: Lỗi tìm kiếm (Retrieval Miss)
1. **Symptom:** User hỏi món ăn cụ thể nhưng Agent trả lời không tìm thấy hoặc trả về món không liên quan.
2. **Why 1:** Tại sao không tìm thấy? -> Vector DB không trả về kết quả có điểm tương đồng cao.
3. **Why 2:** Tại sao điểm tương đồng thấp? -> Từ khóa trong câu hỏi (ví dụ: "giảm cân") không xuất hiện trong metadata của món ăn.
4. **Why 3:** Tại sao metadata thiếu? -> Quy trình gán nhãn dữ liệu (indexing) còn thủ công và chưa bao quát.
5. **Why 4:** Tại sao không bao quát? -> Chiến lược Chunking cố định làm mất ngữ nghĩa.
6. **Root Cause:** Hệ thống thiếu bước **Query Expansion** (mở rộng truy vấn) để hiểu các từ đồng nghĩa.

### Case #2: Yêu cầu "Michelin" giá rẻ (Query: "Tôi muốn ăn Michelin stars mà giá dưới 50k")
1. **Symptom:** Agent gợi ý món "Gỏi Cuốn" và khẳng định giá 50k là hợp lý, bỏ qua hoàn toàn yêu cầu về sao Michelin.
2. **Why 1:** Tại sao Agent bỏ qua từ khóa "Michelin"? -> Vì trong Knowledge Base không có món nào có tag hoặc metadata liên quan đến "Michelin" để hệ thống khớp dữ liệu.
3. **Why 2:** Tại sao không có tag mà Agent vẫn cố trả lời? -> Vì Agent được lập trình để luôn ưu tiên việc hỗ trợ người dùng thay vì từ chối yêu cầu.
4. **Why 3:** Tại sao Agent không biết Michelin là tiêu chuẩn cao cấp? -> Vì LLM không được cung cấp đủ kiến thức về các tiêu chuẩn ẩm thực thế giới trong System Prompt.
5. **Why 4:** Tại sao không có ngưỡng lọc (threshold) cho kết quả tìm kiếm? -> Vì hệ thống Retrieval hiện tại mặc định trả về kết quả Top-K tốt nhất bất kể độ tương đồng thực tế thấp.
6. **Why 5:** Tại sao không có bước kiểm soát chất lượng đầu ra? -> Do kiến trúc hệ thống thiếu lớp "Verification" để so sánh yêu cầu của user với nội dung context trước khi trả lời.
7. **Root Cause:** **Thiếu cơ chế nhận diện thông tin nằm ngoài phạm vi kiến thức (OOD) và lớp kiểm soát logic đầu ra (Output Verification).**

### Case #3: Yêu cầu về chế độ ăn đặc biệt (Query: "Tôi là vegan, kiêng gluten, dị ứng hạt...")
1. **Symptom:** Agent gợi ý món Salad Rau Củ nhưng không thể xác nhận độ an toàn tuyệt đối về Gluten và thành phần mắm.
2. **Why 1:** Tại sao Agent không chắc chắn? -> Vì trong context trả về chỉ có mô tả chung chung, không liệt kê chi tiết từng thành phần gia vị.
3. **Why 2:** Tại sao dữ liệu thiếu chi tiết? -> Vì cấu trúc Knowledge Base (JSON) hiện tại chỉ tập trung vào thông tin thương mại, chưa có cấu trúc dữ liệu kỹ thuật về thành phần.
4. **Why 3:** Tại sao không thể suy luận từ tên món? -> Vì LLM không có đủ dữ liệu về quy trình chế biến thực tế của nhà hàng (ví dụ: sốt salad có chứa mắm hay không).
5. **Why 4:** Tại sao không có bộ quy tắc an toàn cho người dị ứng? -> Hệ thống chưa được tích hợp lớp Logic Guardrails để xử lý các yêu cầu nhạy cảm liên quan đến sức khỏe.
6. **Why 5:** Tại sao kiến trúc chưa hỗ trợ Guardrails? -> Do thiết kế ban đầu chỉ tập trung vào tính năng gợi ý món ăn cơ bản, chưa tính đến các kịch bản người dùng có hạn chế đặc biệt.
7. **Root Cause:** **Dữ liệu Knowledge Base quá mỏng và thiếu lớp Guardrails chuyên biệt cho an toàn thực phẩm.**

## 4. Kế hoạch cải tiến (Action Plan)
- [ ] **P0:** Cập nhật Knowledge Base: Gán thêm các tag metadata như `Dễ tiêu hóa`, `Đồ nóng`, `Đồ lạnh`, `Giảm cân`.
- [ ] **P0:** Triển khai **Hybrid Search** (kết hợp Keyword + Semantic Search) để giảm lỗi Retrieval.
- [ ] **P1:** Thêm bước **Reranking** để sắp xếp lại kết quả tìm kiếm dựa trên độ phù hợp thực tế với câu hỏi.
- [ ] **P1:** Bổ sung **System Prompt** với bộ quy tắc an toàn (ví dụ: "Nếu user đau bụng, tuyệt đối không gợi ý đồ sống/lạnh").

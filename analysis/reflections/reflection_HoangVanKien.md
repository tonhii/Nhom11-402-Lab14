# Reflection - Lab Day 14

**Họ và tên:** Hoàng Văn Kiên  
**MSSV:** 2A202600077  
**Vai trò trong nhóm:** Data Architect (SDG, Golden Dataset Builder)

---

## 1. Mục tiêu & Phân công

**Vai trò:** Data Architect  
**Trách nhiệm chính:**
- Xây dựng bộ **Golden Dataset (50+ cases)** chất lượng cao
- Viết logic sinh dữ liệu tổng hợp (Synthetic Data Generation)
- Gán `ground_truth_ids` cho từng câu hỏi để phục vụ Retrieval Evaluation
- Bao gồm các Red Teaming cases (adversarial, edge cases, contradictions)

**Tệp tin chính:** `data/synthetic_gen.py`  
**Output:** `data/golden_set.jsonl` (50 test cases)

---

## 2. Nội dung công việc đã thực hiện

### 2.1 Xây dựng Knowledge Base
- **Số lượng:** 10 món ăn Việt Nam tiêu biểu
- **Danh sách:** Phở Bò, Bánh Mì, Bún Bò Huế, Cơm Tấm, Gỏi Cuốn, Bánh Xèo, Cháo Gà, Mì Quảng, Salad Ức Bơ, Lẩu Thái
- **Mỗi món gồm:**
  - ID (identifier cho ground_truth_ids)
  - Tên Việt Nam
  - Mô tả chi tiết: thành phần, vị cảm, thích hợp cho ai
- **Chiến lược:** Bao phủ đa dạng: từ đồ ăn đường phố (rẻ) → nhà hàng (đắt), từ nhẹ nhàng → nặng nề, từ không cay → cay nồng

### 2.2 Sinh dữ liệu 50 test cases

**Batch 1 (10 cases) - Easy: Sở thích cơ bản**
- Ăn đồ nhẹ buổi sáng → Phở Bò, Cháo Gà
- Bận rộn, cần nhanh → Bánh Mì
- Thích ăn cay → Bún Bò Huế, Lẩu Thái
- Ăn kiêng giảm cân → Gỏi Cuốn, Salad
- Vừa ốm → Cháo Gà

**Batch 2 (10 cases) - Medium: Câu hỏi đa chiều**
- Occasion-based (tiệc, buổi tối, sinh nhật) → Lẩu Thái, Bánh Xèo
- Nutritional (protein, calo, điều dưỡng) → Cơm Tấm, Salad
- Social (ấn tượng bạn, share nhóm) → Gỏi Cuốn, Lẩu Thái
- Time constraint (10 phút) → Bánh Mì
- Health (bộ dạ yếu) → Cháo Gà, Phở Bò
- Fitness (tăng cơ sau gym) → Cơm Tấm, Salad
- Flavor profile (umami, mùi hương) → Phở Bò, Bún Bò Huế

**Batch 3 (10 cases) - Medium+: Biến thể thêm**
- Dietary restrictions (dị ứng, chay) → Limited options
- Ingredient-based (yêu thích mì/bún) → Phở, Bún Bò, Mì Quảng
- Temperature preference (nóng/lạnh) → Gỏi Cuốn, Salad vs Phở, Cháo
- Food safety concerns → Phở, Bánh Mì, Cơm Tấm
- Cultural (must-try, truyền thống) → Phở Bò, Bánh Mì, Gỏi Cuốn

**Batch 4 (15 cases) - Hard & Adversarial: Test giới hạn Agent**
- **Mâu thuẫn:** "Muốn vừa cay vừa không cay" → No single perfect answer
- **Yêu cầu vô lý:** "Chứa cả gluten và không gluten" → Logical impossibility
- **Misleading context:** "Michelin stars giá dưới 50k" → Khôi phục context thực
- **Extreme restrictions:** "Vegan, kiêng gluten, dị ứng hạt, mắm" → Out of scope
- **Out-of-scope:** Đặt hàng, giao hàng, ngôn ngữ khác → Clarify limitations
- **Meta questions:** "Bạn tên gì? Bạn là AI?" → Define boundaries
- **Subjective claims:** "Phở ngon hơn Bún?" → Acknowledge subjectivity
- **Data limitations:** Hỏi về giá, thông tin không có → Admit lack of data

**Batch 5 (5 cases) - Thêm để đủ 50**
- Budget constraints (30k ăn cả bữa)
- Lifestyle (food blogger, photogenic)
- Open-ended questions (cần clarification)

### 2.3 Cấu trúc dữ liệu (JSONL format)

```json
{
  "question": "Tôi thích ăn đồ nhẹ nhàng buổi sáng, dễ tiêu hóa",
  "expected_answer": "Gợi ý: Phở Bò, Cháo Gà",
  "ground_truth_ids": ["pho_bo", "chao_ga"],
  "context": "[Full description of recommended foods]",
  "metadata": {
    "difficulty": "easy|medium|hard",
    "type": "preference-based|nutritional|adversarial|...",
    "batch": 1,
    "index": 1
  }
}
```

**Tại sao cấu trúc này:**
- `ground_truth_ids`: Danh sách ID đúng → So sánh với output Agent → Tính Hit Rate, MRR
- `context`: Đầy đủ mô tả để Retrieval Judge đánh giá
- `metadata`: Phân loại để phân tích failure

### 2.4 Red Teaming Cases (15 hard cases)
- **Mục đích:** Test xem Agent xử lý tốt những tình huống không mong đợi, mâu thuẫn, hay vô lý không
- **Loại adversarial:** contradiction, impossibility, boundary, out-of-scope, extreme_restriction, subjective, metadata_limitation
- **Ý nghĩa:** Giúp phát hiện điểm yếu của Agent sớm, tránh deploy hệ thống chưa sẵn sàng

---

## 3. 📊 Kết quả đạt được (Deliverables)

**File `data/golden_set.jsonl` hoàn thiện:**
- **Số lượng:** 50 test cases (đúng theo spec)
- **Định dạng:** JSONL (mỗi dòng 1 JSON object)
- **Có đầy đủ thông tin:** question, expected_answer, ground_truth_ids, context, metadata
- **Độ khó cân bằng:** Easy (10) + Medium (25) + Hard (15)
- **Loại câu hỏi đa dạng:** 15+ loại (preference, nutritional, occasion, social, adversarial, boundary, data_limitation, v.v.)
- **Red Teaming:** 15 hard cases để test giới hạn
- **Encoding:** UTF-8 (hỗ trợ Tiếng Việt)

| Chỉ số | Giá trị |
|-------|--------|
| Tổng cases | 50 |
| Easy | ~10 (20%) |
| Medium | ~25 (50%) |
| Hard | ~15 (30%) |
| Food items | 10 |
| Ground Truth IDs | 100% |
| Context coverage | 100% |
| Metadata | 100% |

---

## 4. Kỹ thuật & Chiến lược áp dụng

### 4.1 Evolving Prompt Strategy
- **Batch 1:** Câu hỏi đơn giản, rõ ràng (easy baseline)
- **Batch 2-3:** Tăng độ phức tạp, thêm constraints (medium)
- **Batch 4:** Adversarial, mâu thuẫn, out-of-scope (hard)
- **Lợi ích:** Giúp evaluate Agent ở nhiều level, từ basic competency → edge case handling

### 4.2 Data Diversity & Coverage
- **Diversify by dimension:**
  - Time: sáng, trưa, tối, muộn
  - Health: bình thường, ốm, ăn kiêng, fitness
  - Social: một mình, bạn, gia đình, tiệc
  - Budget: rẻ, bình thường, cao cấp
  - Preference: cay, không cay, nhẹ, nặng
- **Lợi ích:** Không bị overfit vào 1-2 scenario, coverage thực tế từ users

### 4.3 Ground Truth Design
- **Không mơ hồ:** Mỗi `ground_truth_ids` rõ ràng, có thể verify được
- **Chấp nhận multiple correct answers:** VD: "Muốn ăn cay" → [bun_bo_hue, lau_thai] (cả 2 đều đúng)
- **Xử lý edge cases:** Hard cases có `ground_truth_ids: []` (không có đáp án perfect) để test Agent nhận ra giới hạn

---

## 5. Bài học & Thách thức

### Điểm tích cực
1. **Data quality matters:** Dữ liệu tốt → Evaluation tin cậy → Quyết định release tin cậy
2. **Adversarial thinking:** Để eval toàn diện, phải suy nghĩ như attacker: "Cách nào để làm Agent fail?"
3. **Systematic approach:** Thay vì random sinh, phân batch theo độ khó → Dễ analyze kết quả
4. **Reusability:** Dataset này có thể dùng lại cho:
   - V1 vs V2 comparison
   - Unit testing (mỗi lần update prompt)
   - Baseline cho các research paper

### Thách thức gặp phải
1. **Semantic ambiguity:** Không lúc nào có duy nhất 1 đáp án "đúng"
   - VD: "Tôi muốn ăn gì vui vẻ?" có thể là Lẩu, Bánh Xèo, hay bất cứ thứ gì
   - Giải pháp: Chấp nhận multiple correct answers, hoặc clarify trong prompt
   
2. **Ground Truth assignment manual & subjective**
   - Phải tự assign `ground_truth_ids` → Có thể sai
   - Giải pháp: Trong thực tế, cần người review (2-3 annotators) và tính inter-rater agreement
   
3. **Balance giữa realism vs coverage**
   - Muốn cover nhiều scenario nhưng cũng muốn data sát thực
   - Hiện tại: Script-based (nhanh nhưng có thể không realistic)
   - Giải pháp: Hybrid approach - script cho structure, LLM cho diverse phrasings
   
4. **Scalability:** Sinh 50 cases thủ công. Nếu cần 500? 5000?
   - Giải pháp: Full automation với LLM generation + automatic ground truth assignment

### 🔧 Cải tiến nếu có thêm thời gian
1. **LLM-based generation:** Gọi GPT/Claude để tự sinh variations → semantic diversity
2. **Manual annotation pass:** QA team review ground_truth_ids correctness
3. **Linguistic diversity:** Hiện tại 1 số câu dùng cấu trúc giống nhau, có thể paraphrase
4. **User study validation:** Lấy sample cases, hỏi real users xem có agree với ground_truth không
5. **Dynamic balancing:** Monitor distribution, nếu thiếu cases nào thì thêm

---

## 6. Impact & Kết luận

**Tại sao dataset này quan trọng:**
- **Đo lường định lượng:** Hit Rate, MRR được tính trên dataset này → Benchmark tin cậy
- **Phát hiện issues:** Failure analysis dựa vào cases bị lỗi → Tìm root cause → Improve
- **Release decision:** Auto-Gate sẽ dùng metrics này để decide Release/Rollback
- **Reproducibility:** Dataset fixed → Các lần run khác nhau vẫn so sánh được

**Điểm chính:**  
> Chất lượng dataset quyết định chất lượng evaluation. Một dataset tốt là nền tảng cho các quyết định kỹ thuật chính xác. Nếu dataset "giả", kết quả evaluation sẽ "giả", và Agent có thể được release với performance thực tế tệ hơn.

---

## 7. Tự đánh giá

**Điểm tự đánh giá:** **8.5/10**

**Lý do:**
- **Hoàn thành toàn bộ requirements:** 50 cases, ground_truth_ids, metadata, Red Teaming
- **Chất lượng cao:** Data đa dạng, có cấu trúc, có adversarial cases
- **Reusable:** Dataset có thể dùng nhiều lần cho different purposes
- **Chưa tối ưu:** Chưa có manual review, chưa có inter-rater agreement check
- **Edge cases:** Một số semantic ambiguity chưa fully resolved

**Nếu có thêm thời gian:** Có thể đạt 9.5/10 nếu add LLM generation + manual review pass.

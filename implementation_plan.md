# 📋 Kế hoạch Phân công Công việc - Lab Day 14 (Nhóm 6 người)

## 🎯 Mục tiêu bài lab
Xây dựng một **AI Evaluation Factory** đạt chuẩn chuyên nghiệp nhằm:
1.  **Đo lường định lượng:** Chuyển từ đánh giá cảm tính sang đánh giá bằng con số cụ thể (Hit Rate, MRR, Accuracy).
2.  **Đảm bảo độ tin cậy:** Sử dụng **Multi-Judge** để giảm thiểu sai lệ (bias) của một model duy nhất.
3.  **Tự động hóa quy trình:** Xây dựng hệ thống chạy song song (Async) và tự động đưa ra quyết định Release/Rollback.
4.  **Phân tích nguyên nhân:** Tìm ra căn nguyên lỗi của Agent (Failure Analysis) để cải thiện tối ưu hệ thống.


## 👥 Phân chia Vai trò & Nhiệm vụ

| Thành viên | Vai trò | Tệp tin đảm nhiệm | Nhiệm vụ chính | Sản phẩm bàn giao (Output) |
| :--- | :--- | :--- | :--- | :--- |
| **Thành viên 1** | **Team Leader** | `main.py`, `agent/main_agent.py` | Quản lý kiến trúc, tích hợp Agent thực tế, viết logic **Auto-Gate** (Approve/Block) và so sánh Delta V1-V2. | Hệ thống tích hợp hoàn chỉnh, Logic Auto-Gate, file `reports/summary.json`. |
| **Thành viên 2** | **Data Architect** | `data/synthetic_gen.py` | Xây dựng bộ **Golden Dataset (50+ cases)**, viết prompt SDG để sinh data chất lượng, bao gồm Ground Truth IDs. | File `data/golden_set.jsonl` (50+ cases) kèm các cases Red Teaming. |
| **Thành viên 3** | **Retrieval Specialist** | `engine/retrieval_eval.py` | Lập trình tính toán **Hit Rate** và **MRR**. Đảm bảo việc ánh xạ giữa `contexts` của Agent và `ground_truth_ids`. | Module Retrieval Eval, Báo cáo chỉ số Hit Rate & MRR trung bình. |
| **Thành viên 4** | **Judge Specialist** | `engine/llm_judge.py` | Triển khai **Multi-Judge Consensus** (gọi song song GPT/Claude), tính Agreement Rate và xử lý xung đột điểm số. | Module Multi-Judge, Báo cáo Agreement Rate & log so sánh giữa các Judge. |
| **Thành viên 5** | **Perf & Async Engineer** | `engine/runner.py` | Tối ưu hóa **Async Runner** để chạy 50 cases < 2 phút. Quản lý việc log **Cost & Token usage**. | Module Runner (Async), Bảng thống kê Performance & Cost usage. |
| **Thành viên 6** | **AI Analyst** | `analysis/failure_analysis.md` | Chạy benchmark, phân cụm lỗi, thực hiện phân tích **5 Whys** cho các ca lỗi và tổng hợp báo cáo cuối cùng. | File `analysis/failure_analysis.md` (đầy đủ nội dung Failure Clustering & 5 Whys). |

---

## 🕒 Kế hoạch Thực hiện (Lộ trình 4 Tiếng)

### 🚀 Giờ 1: Xây dựng Nền móng (Building Foundation)
*   **Thành viên 1:** Thiết lập Repo, tích hợp Agent cũ vào `agent/main_agent.py`.
*   **Thành viên 2:** Viết prompt SDG và sinh xong 50 cases vào `data/golden_set.jsonl`.
*   **Thành viên 3, 4, 5:** Nghiên cứu cấu trúc code trong `engine/` và thống nhất kiểu dữ liệu trả về giữa các module.
*   **Thành viên 6:** Chuẩn bị cấu trúc file `analysis/failure_analysis.md`.

### ⚙️ Giờ 2: Phát triển Module (Core Development)
*   **Thành viên 3:** Hoàn thiện `retrieval_eval.py` và test với dữ liệu mẫu.
*   **Thành viên 4:** Hoàn thiện `llm_judge.py`, tích hợp API key cho ít nhất 2 model.
*   **Thành viên 5:** Viết logic `asyncio.gather` trong `runner.py` để chạy song song.
*   **Thành viên 1:** Viết logic so sánh V1 vs V2 trong `main.py`.

### 📊 Giờ 3: Chạy Benchmark & Phân tích (Evaluation)
*   **Cả nhóm:** Chạy `python main.py` lần 1.
*   **Thành viên 5:** Kiểm tra log Token/Cost, điều chỉnh nếu chi phí quá cao.
*   **Thành viên 1, 6:** So sánh kết quả, nếu Agent tệ (Score < 3.5), Thành viên 1 điều chỉnh Prompt của Agent.
*   **Thành viên 6:** Bắt đầu phân tích các test cases bị lỗi (True Negative).

### 🏆 Giờ 4: Tối ưu & Hoàn thiện (Polishing)
*   **Thành viên 6:** Hoàn tất báo cáo Failure Analysis và 5 Whys.
*   **Thành viên 2:** Thêm các "Red Teaming cases" (câu hỏi khó/bẫy) để thử thách Agent.
*   **Thành viên 1:** Kiểm tra lại tất cả bằng `python check_lab.py`.
*   **Cả nhóm:** Mỗi người tự viết file `reflection_[Tên].md` của cá nhân mình.

---

## ⚠️ Lưu ý Quan trọng
1. **Giao tiếp:** Thành viên 3 (Retrieval) và 4 (Judge) cần thống nhất JSON output để Thành viên 5 (Runner) tổng hợp dễ dàng.
2. **Chi phí:** Nhóm nên test thử with 3-5 cases trước khi chạy full 50 cases để tránh cạn kiệt Credit API.
3. **Độ ưu tiên:** Phải có **Hit Rate/MRR** và **Multi-Judge** (Đây là điều kiện để không bị điểm liệt phần nhóm).

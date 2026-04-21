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
| **Hồ Thị Tố Nhi** | **Team Leader** | `main.py`, `agent/main_agent.py` | Quản lý kiến trúc, tích hợp Agent thực tế, viết logic **Auto-Gate** (Approve/Block) và so sánh Delta V1-V2. | Hệ thống tích hợp hoàn chỉnh, Logic Auto-Gate, file `reports/summary.json`. |
| **Hoàng Văn Kiên** | **Data Architect** | `data/synthetic_gen.py` | Xây dựng bộ **Golden Dataset (50+ cases)**, viết prompt SDG để sinh data chất lượng, bao gồm Ground Truth IDs. | File `data/golden_set.jsonl` (50+ cases) kèm các cases Red Teaming. |
| **Lê Thị Phương** | **Retrieval Specialist** | `engine/retrieval_eval.py` | Lập trình tính toán **Hit Rate** và **MRR**. Đảm bảo việc ánh xạ giữa `contexts` của Agent và `ground_truth_ids`. | Module Retrieval Eval, Báo cáo chỉ số Hit Rate & MRR trung bình. |
| **Đỗ Văn Quyết** | **Judge Specialist** | `engine/llm_judge.py` | Triển khai **Multi-Judge Consensus** (gọi song song GPT/Claude), tính Agreement Rate và xử lý xung đột điểm số. | Module Multi-Judge, Báo cáo Agreement Rate & log so sánh giữa các Judge. |
| **Lê Hoàng Long** | **Perf & Async Engineer** | `engine/runner.py` | Tối ưu hóa **Async Runner** để chạy 50 cases < 2 phút. Quản lý việc log **Cost & Token usage**. | Module Runner (Async), Bảng thống kê Performance & Cost usage. |
| **Hà Hữu An** | **AI Analyst** | `analysis/failure_analysis.md` | Chạy benchmark, phân cụm lỗi, thực hiện phân tích **5 Whys** cho các ca lỗi và tổng hợp báo cáo cuối cùng. | File `analysis/failure_analysis.md` (đầy đủ nội dung Failure Clustering & 5 Whys). |

---

## 🕒 Kế hoạch Thực hiện (Lộ trình 4 Tiếng)

### 🚀 Giờ 1: Xây dựng Nền móng (Building Foundation)
*   **Hồ Thị Tố Nhi:** Thiết lập Repo, tích hợp Agent cũ vào `agent/main_agent.py`.
*   **Hoàng Văn Kiên:** Viết prompt SDG và sinh xong 50 cases vào `data/golden_set.jsonl`.
*   **Lê Thị Phương, Đỗ Văn Quyết, Lê Hoàng Long:** Nghiên cứu cấu trúc code trong `engine/` và thống nhất kiểu dữ liệu trả về giữa các module.
*   **Hà Hữu An:** Chuẩn bị cấu trúc file `analysis/failure_analysis.md`.

### ⚙️ Giờ 2: Phát triển Module (Core Development)
*   **Lê Thị Phương:** Hoàn thiện `retrieval_eval.py` và test với dữ liệu mẫu.
*   **Đỗ Văn Quyết:** Hoàn thiện `llm_judge.py`, tích hợp API key cho ít nhất 2 model.
*   **Lê Hoàng Long:** Viết logic `asyncio.gather` trong `runner.py` để chạy song song.
*   **Hồ Thị Tố Nhi:** Viết logic so sánh V1 vs V2 trong `main.py`.

### 📊 Giờ 3: Chạy Benchmark & Phân tích (Evaluation)
*   **Cả nhóm:** Chạy `python main.py` lần 1.
*   **Lê Hoàng Long:** Kiểm tra log Token/Cost, điều chỉnh nếu chi phí quá cao.
*   **Hồ Thị Tố Nhi, Hà Hữu An:** So sánh kết quả, nếu Agent tệ (Score < 3.5), Hồ Thị Tố Nhi điều chỉnh Prompt của Agent.
*   **Hà Hữu An:** Bắt đầu phân tích các test cases bị lỗi (True Negative).

### 🏆 Giờ 4: Tối ưu & Hoàn thiện (Polishing)
*   **Hà Hữu An:** Hoàn tất báo cáo Failure Analysis và 5 Whys.
*   **Hoàng Văn Kiên:** Thêm các "Red Teaming cases" (câu hỏi khó/bẫy) để thử thách Agent.
*   **Hồ Thị Tố Nhi:** Kiểm tra lại tất cả bằng `python check_lab.py`.
*   **Cả nhóm:** Mỗi người tự viết file `reflection_[Tên].md` của cá nhân mình.

---

## ⚠️ Lưu ý Quan trọng
1. **Giao tiếp:** Thành viên 3 (Retrieval) và 4 (Judge) cần thống nhất JSON output để Thành viên 5 (Runner) tổng hợp dễ dàng.
2. **Chi phí:** Nhóm nên test thử with 3-5 cases trước khi chạy full 50 cases để tránh cạn kiệt Credit API.
3. **Độ ưu tiên:** Phải có **Hit Rate/MRR** và **Multi-Judge** (Đây là điều kiện để không bị điểm liệt phần nhóm).

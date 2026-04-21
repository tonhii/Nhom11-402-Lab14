from typing import List, Dict, Any

class RetrievalEvaluator:
    # Mapping table to link food names in Agent output to IDs in Golden Dataset
    NAME_TO_ID = {
        "Phở Bò": "pho_bo",
        "Bánh Mì Thịt": "banh_mi",
        "Bún Bò Huế": "bun_bo_hue",
        "Cơm Tấm Sườn Bì": "com_tam",
        "Gỏi Cuốn Tôm Thịt": "goi_cuon",
        "Bánh Xèo": "banh_xeo",
        "Cháo Gà": "chao_ga",
        "Mì Quảng": "mi_quang",
        "Salad Ức Bơ": "salad_uc_bo",
        "Lẩu Thái Hải Sản": "lau_thai",
    }

    def __init__(self):
        pass

    def calculate_hit_rate(self, expected_ids: List[str], retrieved_ids: List[str], top_k: int = 3) -> float:
        """
        Tính toán xem ít nhất 1 trong expected_ids có nằm trong top_k của retrieved_ids không.
        Hit Rate @k = (Số câu hỏi có ít nhất 1 tài liệu đúng trong top k) / Tổng số câu hỏi.
        """
        if not expected_ids:
            return 1.0  # Nếu không có ground truth, coi như mặc định đạt (hoặc tính là N/A)
        
        top_retrieved = retrieved_ids[:top_k]
        hit = any(doc_id in top_retrieved for doc_id in expected_ids)
        return 1.0 if hit else 0.0

    def calculate_mrr(self, expected_ids: List[str], retrieved_ids: List[str]) -> float:
        """
        Tính Mean Reciprocal Rank (MRR).
        Tìm vị trí đầu tiên của một expected_id trong retrieved_ids.
        MRR = 1 / rank (vị trí 1-indexed). Nếu không thấy thì là 0.
        """
        if not expected_ids:
            return 0.0
            
        for i, doc_id in enumerate(retrieved_ids):
            if doc_id in expected_ids:
                return 1.0 / (i + 1)
        return 0.0

    def map_contexts_to_ids(self, contexts: List[Any]) -> List[str]:
        """
        Đảm bảo việc ánh xạ giữa `contexts` của Agent và `ground_truth_ids`.
        Hỗ trợ:
        - List[str]: "Tên món: Mô tả" -> Tách tên và map qua NAME_TO_ID.
        - List[dict]: Có trường 'id' hoặc 'doc_id'.
        """
        retrieved_ids = []
        for ctx in contexts:
            if isinstance(ctx, dict):
                doc_id = ctx.get("id") or ctx.get("doc_id")
                if doc_id:
                    retrieved_ids.append(str(doc_id))
            elif isinstance(ctx, str):
                # Xử lý format "Tên Món: Mô tả..."
                if ":" in ctx:
                    name = ctx.split(":")[0].strip()
                    doc_id = self.NAME_TO_ID.get(name)
                    if doc_id:
                        retrieved_ids.append(doc_id)
                    else:
                        # Fallback nếu không map được
                        retrieved_ids.append(ctx)
                else:
                    # Nếu là string trơn, thử map trực tiếp
                    doc_id = self.NAME_TO_ID.get(ctx)
                    retrieved_ids.append(doc_id if doc_id else ctx)
        return retrieved_ids

    async def evaluate_batch(self, dataset: List[Dict], top_k: int = 3) -> Dict:
        """
        Chạy eval cho toàn bộ bộ dữ liệu.
        Dataset cần có:
        - 'ground_truth_ids': List[str] từ Golden Set.
        - 'contexts' hoặc 'retrieved_ids': Dữ liệu từ Agent Response.
        """
        if not dataset:
            return {"avg_hit_rate": 0.0, "avg_mrr": 0.0}

        total_hit_rate = 0.0
        total_mrr = 0.0
        count = 0

        for item in dataset:
            # 1. Lấy Ground Truth IDs
            expected_ids = item.get("ground_truth_ids", [])
            if not expected_ids:
                expected_ids = item.get("expected_retrieval_ids", [])
            
            # 2. Lấy Kết quả Retrieval từ Agent
            retrieved_ids = item.get("retrieved_ids", [])
            
            # 3. Nếu chưa có IDs, thực hiện ánh xạ từ contexts
            if not retrieved_ids:
                contexts = item.get("contexts", [])
                if not contexts and "metadata" in item:
                    # Fallback lấy từ metadata.retrieved_foods (tên món)
                    foods = item["metadata"].get("retrieved_foods", [])
                    retrieved_ids = [self.NAME_TO_ID.get(f, f) for f in foods]
                else:
                    retrieved_ids = self.map_contexts_to_ids(contexts)

            # 4. Tính toán
            total_hit_rate += self.calculate_hit_rate(expected_ids, retrieved_ids, top_k)
            total_mrr += self.calculate_mrr(expected_ids, retrieved_ids)
            count += 1

        if count == 0:
            return {"avg_hit_rate": 0.0, "avg_mrr": 0.0}

        return {
            "avg_hit_rate": round(total_hit_rate / count, 4),
            "avg_mrr": round(total_mrr / count, 4)
        }


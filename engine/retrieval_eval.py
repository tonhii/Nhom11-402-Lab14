from typing import List, Dict

class RetrievalEvaluator:
    def __init__(self):
        pass

    def calculate_hit_rate(self, ground_truth_ids: List[str], retrieved_ids: List[str], top_k: int = 3) -> float:
        """
        Tính toán xem ít nhất 1 trong ground_truth_ids có nằm trong top_k của retrieved_ids không.
        """
        if not ground_truth_ids:
            return 0.0
        
        top_retrieved = retrieved_ids[:top_k]
        hit = any(doc_id in top_retrieved for doc_id in ground_truth_ids)
        return 1.0 if hit else 0.0

    def calculate_mrr(self, ground_truth_ids: List[str], retrieved_ids: List[str]) -> float:
        """
        Tính Mean Reciprocal Rank.
        Tìm vị trí đầu tiên của một ground_truth_id trong retrieved_ids.
        MRR = 1 / position (1-indexed). Nếu không thấy thì là 0.
        """
        if not ground_truth_ids:
            return 0.0

        for i, doc_id in enumerate(retrieved_ids):
            if doc_id in ground_truth_ids:
                return 1.0 / (i + 1)
        return 0.0

    def evaluate(self, ground_truth_ids: List[str], retrieved_ids: List[str]) -> Dict[str, float]:
        """
        Hàm giao tiếp chuẩn: Trả về toàn bộ các chỉ số retrieval.
        """
        return {
            "hit_rate": self.calculate_hit_rate(ground_truth_ids, retrieved_ids),
            "mrr": self.calculate_mrr(ground_truth_ids, retrieved_ids)
        }

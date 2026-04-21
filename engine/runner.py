import asyncio
import time
from typing import List, Dict

class BenchmarkRunner:
    def __init__(self, agent, evaluator, judge, max_concurrent: int = 5):
        self.agent = agent
        self.evaluator = evaluator
        self.judge = judge
        self.semaphore = asyncio.Semaphore(max_concurrent)

    async def run_single_test(self, test_case: Dict) -> Dict:
        async with self.semaphore:
            try:
                start_time = time.perf_counter()
                
                # 1. Gọi Agent
                response = await self.agent.query(test_case["question"])
                latency = time.perf_counter() - start_time
                
                # 2. Chạy Retrieval Evaluation
                # Giả sử agent trả về các ID tài liệu đã tìm thấy
                retrieved_ids = response.get("metadata", {}).get("doc_ids", [])
                hit_rate = self.evaluator.calculate_hit_rate([test_case.get("doc_id")], retrieved_ids)
                mrr = self.evaluator.calculate_mrr([test_case.get("doc_id")], retrieved_ids)

                # 3. Chạy Multi-Judge
                judge_result = await self.judge.evaluate_multi_judge(
                    test_case["question"], 
                    response["answer"], 
                    test_case["expected_answer"]
                )
                
                return {
                    "test_case": test_case["question"],
                    "agent_response": response["answer"],
                    "latency": latency,
                    "retrieval": {"hit_rate": hit_rate, "mrr": mrr},
                    "judge": judge_result,
                    "status": "fail" if judge_result["final_score"] < 3 else "pass"
                }
            except Exception as e:
                print(f"Error running test case: {e}")
                return {"status": "error", "error": str(e)}

    async def run_all(self, dataset: List[Dict]) -> List[Dict]:
        """
        Chạy song song bằng asyncio.gather với Semaphore kiểm soát số lượng.
        """
        tasks = [self.run_single_test(case) for case in dataset]
        results = await asyncio.gather(*tasks)
        # Lọc bỏ các kết quả lỗi nếu cần
        return [r for r in results if r["status"] != "error"]

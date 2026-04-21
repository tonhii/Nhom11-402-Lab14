import os
import json
from typing import List, Dict, Optional
from openai import AsyncOpenAI

from agent.main_agent import MainAgent, load_all_knowledge_bases

class ChunkRetriever:
    """
    Retriever V2: Hybrid Search (Khớp Tag + Khớp Keyword toàn văn bản).
    """
    def __init__(self, knowledge_base: List[Dict]):
        self.chunks = []
        for food in knowledge_base:
            chunk_id = food.get("id", "N/A")
            ingredients = ", ".join(food.get("ingredients", []))
            tags = ", ".join(food.get("tags", []))
            suitable = ", ".join(food.get("suitable_for", []))
            
            chunk_text = (
                f"{food.get('name', '')} "
                f"{food.get('description', '')} "
                f"{ingredients} {tags} {suitable}"
            )
            self.chunks.append({
                "chunk_id": chunk_id,
                "chunk_text": chunk_text,
                "original_food": food
            })

    def _score_chunk(self, chunk: Dict, preferences: Dict) -> float:
        score = 0.0
        text = chunk["chunk_text"].lower()
        food = chunk["original_food"]
        
        # 1. Exact Tag Match (như V1 nhưng điểm cao hơn)
        user_tags = set(preferences.get("tags", []))
        food_tags = set(food.get("tags", []))
        score += len(user_tags & food_tags) * 3.0

        # 2. Calories Target
        max_cal = preferences.get("max_calories")
        if max_cal and food.get("calories", float('inf')) <= max_cal:
            score += 2.0

        # 3. Phạt Restrictions
        for restriction in preferences.get("restrictions", []):
             for not_suit in food.get("not_suitable_for", []):
                    if restriction.lower() in not_suit.lower():
                        score -= 20.0

        # 4. Fuzzy Keyword Match (Tính năng Hybrid Search của V2)
        for hint in preferences.get("free_text_hints", []):
            words = hint.lower().split()
            for word in words:
                if len(word) >= 3 and word in text:
                    score += 2.0

        return score

    def retrieve(self, preferences: Dict, top_k: int = 3) -> List[Dict]:
        scored = [(chunk["original_food"], self._score_chunk(chunk, preferences)) for chunk in self.chunks]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [food for food, score in scored[:top_k] if score > -5]


class MainAgentV2(MainAgent):
    """
    Agent V2: Hybrid Search + CoT Prompt Optimization.
    Sử dụng *cùng bộ dữ liệu* với V1 để đảm bảo Benchmark công bằng (Apples-to-Apples).
    """
    def __init__(self, api_key: Optional[str] = None, kb_path: str = "data/food_knowledge_base.json"):
        self.name = "FoodAgent-RAG-v2"
        self.client = AsyncOpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        
        from agent.main_agent import load_knowledge_base
        # Bắt buộc dùng chung 10 items để so sánh chính xác với Ground Truth của golden_set
        knowledge_base = load_knowledge_base(kb_path)
        self.retriever = ChunkRetriever(knowledge_base)
        
        self.system_prompt = """Bạn là chuyên gia ẩm thực thân thiện và cực kỳ chính xác.
QUY TẮC:
1. GỢI Ý CHÍNH XÁC: Chỉ gợi ý các món ăn được cung cấp trong danh sách RAG.
2. DỄ ĐỌC: Trả lời tự nhiên: "Dựa trên sở thích của bạn, tôi gợi ý: [Tên các món ăn]".
3. GIẢI THÍCH NGẮN GỌN: Nêu bật đặc điểm phù hợp nhất của món đó với câu hỏi.
4. KHÔNG ẢO GIÁC: Nếu không có món nào thỏa mãn rủi ro dị ứng/sức khỏe, hãy nói: "Xin lỗi, hiện tại không có lựa chọn phù hợp hoàn hảo, nhưng bạn cân nhắc món..."."""

    async def _generate_recommendation(self, user_question: str, retrieved_foods: List[Dict]) -> str:
        if not retrieved_foods:
            return "Xin lỗi, tôi không có lựa chọn phù hợp."
            
        context_parts = []
        for food in retrieved_foods:
            context_parts.append(
                f"- Tên món: {food.get('name', 'N/A')}\n"
                f"  Mô tả: {food.get('description', '')}\n"
                f"  Phù hợp: {', '.join(food.get('suitable_for', []))}"
            )
        context = "\n".join(context_parts)
        
        rag_prompt = f"""Ngữ cảnh món ăn (RAG):
{context}

Câu hỏi: "{user_question}"

Dựa trên Câu hỏi và Ngữ cảnh, hãy viết câu trả lời tốt nhất. Đừng dài dòng."""

        response = await self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": rag_prompt},
            ],
            temperature=0.3,
            max_completion_tokens=400,
        )
        return response.choices[0].message.content

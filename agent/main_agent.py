import asyncio
import json
import os
from pathlib import Path
from typing import List, Dict, Optional
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()
# ============================================================
# LOAD KNOWLEDGE BASE từ file JSON
# ============================================================

def load_knowledge_base(path: str = "../data/food_knowledge_base.json") -> List[Dict]:
    """
    Đọc knowledge base từ file JSON bên ngoài.
    Dễ dàng thêm/sửa/xóa món mà không cần chạm vào code.
    """
    kb_path = Path(path)
    if not kb_path.exists():
        raise FileNotFoundError(
            f"Không tìm thấy file knowledge base: '{path}'\n"
            f"Hãy đặt file food_knowledge_base.json cùng thư mục với script này."
        )
    with open(kb_path, encoding="utf-8") as f:
        data = json.load(f)
    print(f"✅ Đã load {len(data)} món ăn từ '{kb_path.resolve()}'")
    return data


# ============================================================
# RETRIEVER - Tầng tìm kiếm của RAG
# ============================================================

class FoodRetriever:
    """
    Retriever dùng keyword matching + tag scoring.
    Trong thực tế có thể swap bằng ChromaDB + embedding thật.
    """

    def __init__(self, knowledge_base: List[Dict]):
        self.kb = knowledge_base

    def _score(self, food: Dict, preferences: Dict) -> float:
        score = 0.0
        user_tags = set(preferences.get("tags", []))
        food_tags = set(food["tags"])
        score += len(user_tags & food_tags) * 2.0

        max_cal = preferences.get("max_calories")
        if max_cal and food["calories"] <= max_cal:
            score += 1.5

        for restriction in preferences.get("restrictions", []):
            for not_suit in food.get("not_suitable_for", []):
                if restriction.lower() in not_suit.lower():
                    score -= 5.0

        for hint in preferences.get("free_text_hints", []):
            for suit in food.get("suitable_for", []):
                if any(word in suit.lower() for word in hint.lower().split()):
                    score += 1.0

        return score

    def retrieve(self, preferences: Dict, top_k: int = 3) -> List[Dict]:
        scored = [(food, self._score(food, preferences)) for food in self.kb]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [food for food, score in scored[:top_k] if score > -3]


# ============================================================
# MAIN AGENT - Tích hợp RAG + OpenAI
# ============================================================

class MainAgent:
    """
    Agent gợi ý đồ ăn sử dụng kiến trúc RAG:
    1. Load knowledge base từ file JSON
    2. Retrieval: Tìm món phù hợp từ knowledge base
    3. Generation: Dùng OpenAI để sinh gợi ý tự nhiên
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        kb_path: str = "../data/food_knowledge_base.json",
    ):
        self.name = "FoodAgent-RAG-v1"
        self.client = AsyncOpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        knowledge_base = load_knowledge_base(kb_path)
        self.retriever = FoodRetriever(knowledge_base)
        self.system_prompt = """Bạn là một chuyên gia ẩm thực Việt Nam thân thiện.
Nhiệm vụ của bạn là gợi ý món ăn dựa trên các món đã được tìm kiếm từ cơ sở tri thức.
Hãy trả lời tự nhiên, sinh động và hữu ích bằng tiếng Việt.
Luôn giải thích TẠI SAO món đó phù hợp với người dùng.
Nếu có thể, thêm 1-2 mẹo nhỏ khi thưởng thức món đó."""

    async def _extract_preferences(self, user_input: str) -> Dict:
        extraction_prompt = f"""Phân tích câu hỏi sau và trả về JSON với các trường:
- tags: list các tag phù hợp (chọn từ: mặn, cay, ngọt, nhẹ, giòn, béo, nóng, tươi mát, lành mạnh, ít calo, no lâu, nhanh, bữa sáng, bữa trưa, bữa tối, ăn kiêng, hải sản, truyền thống)
- max_calories: số calo tối đa (null nếu không đề cập)
- restrictions: list các hạn chế (vd: ăn chay, dị ứng hải sản, kiêng cay)
- free_text_hints: list các gợi ý tự do khác

Câu hỏi: "{user_input}"

Chỉ trả về JSON, không giải thích thêm."""

        response = await self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": extraction_prompt}],
            temperature=0,
            response_format={"type": "json_object"},
        )
        return json.loads(response.choices[0].message.content)

    async def _generate_recommendation(self, user_question: str, retrieved_foods: List[Dict]) -> str:
        context_parts = []
        for i, food in enumerate(retrieved_foods, 1):
            context_parts.append(
                f"[Món {i}] {food['name']}\n"
                f"  Mô tả: {food['description']}\n"
                f"  Calo: {food['calories']} kcal\n"
                f"  Phù hợp: {', '.join(food['suitable_for'])}\n"
                f"  Nguyên liệu chính: {', '.join(food['ingredients'][:4])}"
            )
        context = "\n\n".join(context_parts)
        rag_prompt = f"""Dựa trên các món ăn sau đây từ cơ sở dữ liệu:

{context}

Hãy gợi ý cho người dùng có câu hỏi: "{user_question}"

Trả lời ngắn gọn, thân thiện và thực tế."""

        response = await self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": rag_prompt},
            ],
            temperature=0.7,
            max_tokens=600,
        )
        return response.choices[0].message.content

    async def query(self, question: str) -> Dict:
        """Pipeline RAG: Extract preferences → Retrieve → Generate."""
        preferences = await self._extract_preferences(question)
        retrieved_foods = self.retriever.retrieve(preferences, top_k=3)

        if not retrieved_foods:
            return {
                "answer": "Xin lỗi, mình không tìm thấy món nào phù hợp. Bạn thử mô tả lại khẩu vị nhé!",
                "contexts": [],
                "metadata": {"retrieved_count": 0},
            }

        answer = await self._generate_recommendation(question, retrieved_foods)
        return {
            "answer": answer,
            "contexts": [f"{food['name']}: {food['description']}" for food in retrieved_foods],
            "metadata": {
                "model": "gpt-4o-mini",
                "retrieved_count": len(retrieved_foods),
                "retrieved_ids": [f["id"] for f in retrieved_foods],
                "extracted_preferences": preferences,
                "sources": ["food_knowledge_base.json"],
            },
        }


# ============================================================
# DEMO
# ============================================================

async def demo():
    agent = MainAgent(kb_path="data/food_knowledge_base.json")

    test_questions = [
        "Tôi muốn ăn gì đó nhẹ nhàng, không cay, buổi sáng nay?",
        "Đang ăn kiêng giảm cân, gợi ý món nào ít calo không?",
        "Trời lạnh muốn ăn gì nóng và no lâu?",
        "Tôi bị dị ứng hải sản, có món truyền thống nào ngon không?",
    ]

    print("=" * 60)
    print(f"🍜 {agent.name} - Demo RAG Food Recommendation")
    print("=" * 60)

    for q in test_questions:
        print(f"\n❓ Câu hỏi: {q}")
        print("-" * 40)
        result = await agent.query(q)
        print(f"💬 Gợi ý:\n{result['answer']}")
        print(f"\n📚 Nguồn ({len(result['contexts'])} món):")
        for ctx in result["contexts"]:
            print(f"  • {ctx[:80]}...")
        print(f"\n🔧 Metadata: {result['metadata']}")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(demo())
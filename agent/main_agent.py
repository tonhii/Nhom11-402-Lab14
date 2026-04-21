import asyncio
import json
import os
from typing import List, Dict, Optional
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()
# ============================================================
# KNOWLEDGE BASE - "Cơ sở tri thức" cho RAG
# Trong thực tế, phần này có thể là vector DB (Chroma, Pinecone...)
# ============================================================

FOOD_KNOWLEDGE_BASE = [
    {
        "id": "pho_bo",
        "name": "Phở Bò",
        "tags": ["mặn", "nước", "nóng", "bữa sáng", "bữa trưa", "truyền thống", "nhẹ bụng"],
        "calories": 400,
        "ingredients": ["bánh phở", "thịt bò", "xương bò", "hành", "gừng", "gia vị"],
        "description": "Phở bò truyền thống với nước dùng trong, thơm ngọt từ xương ninh lâu.",
        "suitable_for": ["người thích ăn nhẹ", "người ăn sáng", "người thích vị umami"],
        "not_suitable_for": ["người ăn chay", "người kiêng gluten"],
    },
    {
        "id": "banh_mi",
        "name": "Bánh Mì Thịt",
        "tags": ["mặn", "giòn", "nhanh", "bữa sáng", "tiện lợi", "đường phố"],
        "calories": 350,
        "ingredients": ["bánh mì", "thịt nguội", "pate", "rau sống", "tương ớt"],
        "description": "Bánh mì Việt Nam với vỏ giòn, nhân thịt phong phú, ăn nhanh tiện lợi.",
        "suitable_for": ["người bận rộn", "người thích ăn nhanh", "buổi sáng"],
        "not_suitable_for": ["người ăn chay", "người kiêng tinh bột"],
    },
    {
        "id": "bun_bo_hue",
        "name": "Bún Bò Huế",
        "tags": ["cay", "đậm đà", "nước", "nóng", "bữa sáng", "bữa trưa", "miền Trung"],
        "calories": 450,
        "ingredients": ["bún", "thịt bò", "giò heo", "mắm ruốc", "sả", "ớt"],
        "description": "Bún bò cay nồng đặc trưng Huế, nước dùng đậm vị mắm ruốc và sả.",
        "suitable_for": ["người thích ăn cay", "người thích hương vị đậm đà"],
        "not_suitable_for": ["người không ăn được cay", "người ăn chay"],
    },
    {
        "id": "com_tam",
        "name": "Cơm Tấm Sườn Bì",
        "tags": ["mặn", "ngọt", "bữa trưa", "bữa tối", "no lâu", "đường phố"],
        "calories": 600,
        "ingredients": ["cơm tấm", "sườn nướng", "bì", "chả trứng", "nước mắm"],
        "description": "Cơm tấm Sài Gòn với sườn nướng thơm lừng, bì giòn, ăn kèm nước mắm chua ngọt.",
        "suitable_for": ["người cần ăn no", "bữa chính", "người thích thịt nướng"],
        "not_suitable_for": ["người ăn chay", "người kiêng calo cao"],
    },
    {
        "id": "goi_cuon",
        "name": "Gỏi Cuốn Tôm Thịt",
        "tags": ["nhẹ", "tươi mát", "lành mạnh", "ít calo", "không cay", "khai vị"],
        "calories": 200,
        "ingredients": ["bánh tráng", "tôm", "thịt heo", "rau sống", "bún", "tương hoisin"],
        "description": "Gỏi cuốn tươi mát, nhẹ nhàng, ăn kèm tương chấm đậu phộng.",
        "suitable_for": ["người ăn kiêng", "người thích ăn nhẹ", "thời tiết nóng", "người giảm cân"],
        "not_suitable_for": ["người dị ứng hải sản"],
    },
    {
        "id": "banh_xeo",
        "name": "Bánh Xèo",
        "tags": ["giòn", "béo", "bữa chiều", "bữa tối", "đặc sản", "miền Nam"],
        "calories": 500,
        "ingredients": ["bột gạo", "tôm", "thịt heo", "giá đỗ", "hành lá", "nước cốt dừa"],
        "description": "Bánh xèo giòn tan, nhân tôm thịt béo ngậy, cuốn rau sống chấm nước mắm.",
        "suitable_for": ["người thích ăn giòn", "ăn chơi buổi chiều", "bữa tối gia đình"],
        "not_suitable_for": ["người kiêng dầu mỡ", "người dị ứng hải sản"],
    },
    {
        "id": "chao_ga",
        "name": "Cháo Gà",
        "tags": ["mềm", "dễ ăn", "nóng", "bổ dưỡng", "dễ tiêu", "bữa sáng", "người bệnh"],
        "calories": 280,
        "ingredients": ["gạo", "thịt gà", "gừng", "hành lá", "tiêu"],
        "description": "Cháo gà nóng hổi, mềm mịn, thơm mùi gừng, dễ tiêu hóa và bổ dưỡng.",
        "suitable_for": ["người bệnh", "người mới ốm dậy", "người tiêu hóa kém", "buổi sáng lạnh"],
        "not_suitable_for": ["người ăn chay"],
    },
    {
        "id": "mi_quang",
        "name": "Mì Quảng",
        "tags": ["đậm đà", "ít nước", "bữa trưa", "miền Trung", "đặc sản", "no lâu"],
        "calories": 480,
        "ingredients": ["mì Quảng", "tôm", "thịt heo", "trứng cút", "đậu phộng", "bánh tráng nướng"],
        "description": "Mì Quảng ít nước đặc trưng Đà Nẵng, ăn kèm bánh tráng nướng giòn và rau sống.",
        "suitable_for": ["người thích ăn no", "người thích hương vị miền Trung"],
        "not_suitable_for": ["người dị ứng hải sản", "người ăn chay"],
    },
    {
        "id": "salad_uc_bơ",
        "name": "Salad Ức Bơ",
        "tags": ["lành mạnh", "ít calo", "tươi mát", "ăn kiêng", "không cay", "bữa trưa"],
        "calories": 250,
        "ingredients": ["ức gà nướng", "bơ", "cà chua", "rau xanh", "dầu olive", "chanh"],
        "description": "Salad ức gà bơ thanh mát, giàu protein và chất béo lành mạnh, phù hợp ăn kiêng.",
        "suitable_for": ["người ăn kiêng", "người tập gym", "người thích ăn sạch", "giảm cân"],
        "not_suitable_for": ["người không thích rau sống"],
    },
    {
        "id": "lau_thai",
        "name": "Lẩu Thái Hải Sản",
        "tags": ["cay", "chua", "nóng", "hải sản", "bữa tối", "nhóm bạn", "đặc biệt"],
        "calories": 550,
        "ingredients": ["tôm", "mực", "ngao", "nấm", "sả", "ớt", "me", "lá chanh"],
        "description": "Lẩu Thái chua cay nồng nàn với hải sản tươi, hương thơm sả ớt đặc trưng.",
        "suitable_for": ["người thích cay", "ăn cùng bạn bè", "bữa tối cuối tuần"],
        "not_suitable_for": ["người dị ứng hải sản", "người không ăn được cay"],
    },
]

# ============================================================
# RETRIEVER - Tầng tìm kiếm của RAG
# ============================================================

class FoodRetriever:
    """
    Retriever đơn giản dùng keyword matching + tag scoring.
    Trong thực tế có thể thay bằng embedding + cosine similarity.
    """
    def __init__(self, knowledge_base: List[Dict]):
        self.kb = knowledge_base

    def _score(self, food: Dict, preferences: Dict) -> float:
        """Tính điểm phù hợp giữa món ăn và khẩu vị user."""
        score = 0.0

        # Khớp tags với sở thích
        user_tags = set(preferences.get("tags", []))
        food_tags = set(food["tags"])
        tag_overlap = len(user_tags & food_tags)
        score += tag_overlap * 2.0

        # Kiểm tra calo
        max_cal = preferences.get("max_calories")
        if max_cal and food["calories"] <= max_cal:
            score += 1.5

        # Tránh đồ ăn không phù hợp
        restrictions = preferences.get("restrictions", [])
        for restriction in restrictions:
            for not_suit in food.get("not_suitable_for", []):
                if restriction.lower() in not_suit.lower():
                    score -= 5.0  # Penalty nặng

        # Khớp suitable_for
        for pref in preferences.get("free_text_hints", []):
            for suit in food.get("suitable_for", []):
                if any(word in suit.lower() for word in pref.lower().split()):
                    score += 1.0

        return score

    def retrieve(self, preferences: Dict, top_k: int = 3) -> List[Dict]:
        """Trả về top_k món ăn phù hợp nhất."""
        scored = [
            (food, self._score(food, preferences))
            for food in self.kb
        ]
        scored.sort(key=lambda x: x[1], reverse=True)
        top = [food for food, score in scored[:top_k] if score > -3]
        return top


# ============================================================
# MAIN AGENT - Tích hợp RAG + OpenAI
# ============================================================

class MainAgent:
    """
    Agent gợi ý đồ ăn sử dụng kiến trúc RAG:
    1. Hỏi khẩu vị người dùng (multi-turn)
    2. Retrieval: Tìm món phù hợp từ knowledge base
    3. Generation: Dùng OpenAI để sinh gợi ý tự nhiên
    """

    def __init__(self, api_key: Optional[str] = None):
        self.name = "FoodAgent-RAG-v1"
        self.client = AsyncOpenAI(
            api_key=api_key or os.getenv("OPENAI_API_KEY")
        )
        self.retriever = FoodRetriever(FOOD_KNOWLEDGE_BASE)

        # System prompt cho LLM
        self.system_prompt = """Bạn là một chuyên gia ẩm thực Việt Nam thân thiện.
Nhiệm vụ của bạn là gợi ý món ăn dựa trên các món đã được tìm kiếm từ cơ sở tri thức.
Hãy trả lời tự nhiên, sinh động và hữu ích bằng tiếng Việt.
Luôn giải thích TẠI SAO món đó phù hợp với người dùng.
Nếu có thể, thêm 1-2 mẹo nhỏ khi thưởng thức món đó."""

    async def _extract_preferences(self, user_input: str) -> Dict:
        """
        Dùng LLM để trích xuất structured preferences từ câu hỏi tự do của user.
        Đây là bước 'understanding' trước khi Retrieve.
        """
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
        raw = response.choices[0].message.content
        return json.loads(raw)

    async def _generate_recommendation(
        self,
        user_question: str,
        retrieved_foods: List[Dict],
    ) -> str:
        """
        Generation step: Dùng OpenAI để sinh câu trả lời dựa trên context đã retrieve.
        """
        # Chuẩn bị context từ retrieved documents
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
        """
        Pipeline RAG hoàn chỉnh:
        1. Extract preferences từ câu hỏi
        2. Retrieve: Tìm món phù hợp
        3. Generate: Sinh gợi ý tự nhiên
        """
        # --- Bước 1: Hiểu ý định người dùng ---
        preferences = await self._extract_preferences(question)

        # --- Bước 2: Retrieval ---
        retrieved_foods = self.retriever.retrieve(preferences, top_k=3)

        if not retrieved_foods:
            return {
                "answer": "Xin lỗi, mình không tìm thấy món nào phù hợp với yêu cầu của bạn. Bạn thử mô tả lại khẩu vị nhé!",
                "contexts": [],
                "metadata": {"retrieved_count": 0},
            }

        # --- Bước 3: Generation ---
        answer = await self._generate_recommendation(question, retrieved_foods)

        return {
            "answer": answer,
            "contexts": [
                f"{food['name']}: {food['description']}"
                for food in retrieved_foods
            ],
            "metadata": {
                "model": "gpt-4o-mini",
                "retrieved_count": len(retrieved_foods),
                "retrieved_ids": [f["id"] for f in retrieved_foods],
                "extracted_preferences": preferences,
                "sources": ["food_knowledge_base"],
            },
        }


# ============================================================
# DEMO - Thử nghiệm agent
# ============================================================

async def demo():
    agent = MainAgent()  # Dùng OPENAI_API_KEY từ env

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
        print(f"\n📚 Nguồn tham khảo ({len(result['contexts'])} món):")
        for ctx in result["contexts"]:
            print(f"  • {ctx[:80]}...")
        print(f"\n🔧 Metadata: {result['metadata']}")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(demo())
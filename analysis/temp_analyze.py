import json

with open('reports/benchmark_results.json', encoding='utf-8') as f:
    data = json.load(f)

fails = []
for item in data:
    judge = item.get('judge', {})
    if isinstance(judge, dict):
        score = judge.get('final_score', 5.0)
        if score <= 2.5:
            fails.append({
                "id": item["test_case"]["index"],
                "q": item["test_case"]["question"],
                "ans": item["agent_response"],
                "score": score
            })

print(f"Total severe fails (<=2.5): {len(fails)}")
for f in fails[:5]:
    print(f"Q{f['id']}: {f['q']}")
    print(f"Ans: {f['ans']}")
    print(f"Score: {f['score']}\n")

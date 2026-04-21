import json

def cluster_failures(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    clusters = {
        'Retrieval Miss': [],
        'Hallucination': [],
        'Low Relevancy': [],
        'Constraint/Logic Error': []
    }
    
    for item in data:
        if item.get('status') == 'fail':
            ragas = item.get('ragas', {})
            retrieval = ragas.get('retrieval', {})
            
            # Logic for clustering
            if retrieval.get('hit_rate', 0) == 0:
                clusters['Retrieval Miss'].append(item)
            elif ragas.get('faithfulness', 1) < 0.85:
                clusters['Hallucination'].append(item)
            elif ragas.get('relevancy', 1) < 0.8:
                clusters['Low Relevancy'].append(item)
            else:
                clusters['Constraint/Logic Error'].append(item)
                
    print(f"Total Fails: {sum(len(v) for v in clusters.values())}")
    for group, items in clusters.items():
        print(f"{group}: {len(items)}")

if __name__ == "__main__":
    cluster_failures('d:/VinAction/Nhom11-402-Lab14/reports/benchmark_results.json')

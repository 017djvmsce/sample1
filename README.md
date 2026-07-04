import sys
from collections import defaultdict

def main():
    graph = defaultdict(list)
    nodes = set()
    
    # 【本番仕様】標準入力（sys.stdin）からすべてのテストデータを1行ずつ読み込む
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        
        parts = line.split(',')
        if len(parts) != 3:
            continue
            
        u = int(parts[0].strip())
        v = int(parts[1].strip())
        weight = float(parts[2].strip())
        
        graph[u].append((v, weight))
        graph[v].append((u, weight))
        nodes.add(u)
        nodes.add(v)
    
    max_distance = -1.0
    best_path = []

    def dfs(current_node, current_dist, visited, current_path):
        nonlocal max_distance, best_path
        
        if current_dist > max_distance:
            max_distance = current_dist
            best_path = list(current_path)
            
        for next_node, weight in graph[current_node]:
            if next_node not in visited:
                visited.add(next_node)
                current_path.append(next_node)
                
                dfs(next_node, current_dist + weight, visited, current_path)
                
                current_path.pop()
                visited.remove(next_node)

    for start_node in nodes:
        visited_set = {start_node}
        dfs(start_node, 0.0, visited_set, [start_node])

    # 【本番仕様】余計な文字（"総距離"など）を入れず、IDだけを純粋に改行区切りで出力する
    for node_id in best_path:
        print(node_id)

if __name__ == '__main__':
    main()

import networkx as nx
import math

# Haversine 거리 계산 함수 (위도, 경도 튜플 두 개 입력)
def haversine(coord1, coord2):
    # 지구 반지름 (km)
    R = 6371
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# 1. 노드 좌표 정의
locations = {
    "A": (37.5547, 126.9706),  # 서울역
    "B": (37.5796, 126.9770),  # 경복궁
    "C": (37.5572, 126.9245),  # 홍대입구
    "D": (37.4979, 127.0276),  # 강남역
    "E": (37.5110, 127.0980),  # 잠실
    "F": (37.5349, 126.9946),  # 이태원 
    "G": (37.5826, 126.9830),  # 북촌한옥마을 
    "H": (37.5663, 127.0094)   # 동대문디자인플라자 
}

# 2. 그래프 생성 및 간선 추가
graph = nx.Graph()

# 노드 추가
for node in locations:
    graph.add_node(node, pos=locations[node])

# 막힌 도로(서울역→경복궁) 일부러 긴 거리 부여
graph.add_edge("A", "B", weight=999)

# 실제 거리 기반 연결 (예시)
graph.add_edge("A", "C", weight=haversine(locations["A"], locations["C"]))
graph.add_edge("C", "D", weight=haversine(locations["C"], locations["D"]))
graph.add_edge("D", "E", weight=haversine(locations["D"], locations["E"]))
graph.add_edge("E", "B", weight=haversine(locations["E"], locations["B"]))

# 3. 다익스트라 알고리즘으로 최단 경로 계산
path = nx.dijkstra_path(graph, "A", "B", weight="weight")
length = nx.dijkstra_path_length(graph, "A", "B", weight="weight")

print("서울역(A) → 경복궁(B) 다익스트라 최단경로:", path)
print("총 거리 (km):", round(length, 2))

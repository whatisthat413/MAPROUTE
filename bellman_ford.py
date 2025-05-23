import math
import sys
sys.stdout.reconfigure(encoding='utf-8')
#인코딩 문제 해결 

class Graph:
    def __init__(self, vertices):
        self.vertices = vertices
        self.edges = []
        # 그래프 클래스 정의
        # __init__ 함수에서 정점 목록(vertices)을 받고, 간선 저장할 빈 리스트(edges) 초기화

    def add_edge(self, src, dest, weight):
        self.edges.append((src, dest, weight))
        # add_edge 함수는 두 정점과 가중치를 받아서 엣지 리스트에 추가함

    def bellman_ford(self, start):
        distance = {v: float("inf") for v in self.vertices}
        predecessor = {v: None for v in self.vertices}  # 최단 경로를 저장할 딕셔너리
        distance[start] = 0
        # 벨만포드 알고리즘, 시작 정점에서 모든 정점까지의 최단거리 계산
        # 일단 모든 정점 거리 무한(inf)으로 설정, 시작 정점은 0으로

        for _ in range(len(self.vertices) - 1):
            for src, dest, weight in self.edges:
                if distance[src] + weight < distance[dest]:
                    distance[dest] = distance[src] + weight
                    predecessor[dest] = src  # 최단 경로를 저장
        # 모든 간선 검사하여 거리값을 업데이트

        for src, dest, weight in self.edges:
            if distance[src] + weight < distance[dest]:
                raise ValueError("음수 사이클이 존재합니다.")
        # 음수 사이클 확인, 한 번 더 간선 확인 후 거리 업데이트가 가능한 경우, 음수 사이클 존재한다고 판단

        return distance, predecessor  # predecessor도 반환

    def get_path(self, start, end, predecessor):
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = predecessor[current]
        path.reverse()  # 경로를 올바른 순서로 정렬
        return path  # 최단 경로 반환

def haversine(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    R = 6371  # km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c
# 해버사인 공식 (위도·경도로 구의 표면상 거리 구하는 삼각함수 공식)

locations = {
    "A": (37.5547, 126.9706),  # 서울역
    "B": (37.5796, 126.9770),  # 경복궁
    "C": (37.5572, 126.9245)   # 홍대입구
}
# 위도 경도

graph = Graph(locations.keys())
# 위의 좌표 키로 그래프 생성

for src in locations:
    for dest in locations:
        if src != dest:
            graph.add_edge(src, dest, haversine(locations[src], locations[dest]))
# 모든 지점들 간 거리 계산 후 간선 추가
# src != dest = 자기 자신으로 가는 경로 제외

start_point = "A"
distances, predecessors = graph.bellman_ford(start_point)  # predecessors도 반환받음
# 시작 지점 A로 설정

print(f"{start_point}에서 각 점까지의 최단 거리:")
for point, dist in distances.items():
    print(f"{point}: {dist:.2f} km")

print("\n최단 경로 출력:")  # 최단 경로 출력 기능 추가
for point in locations.keys():
    if point != start_point:
        path = graph.get_path(start_point, point, predecessors)
        print(f"{start_point} → {point}: {' → '.join(path)}")


# A → B: A → B / A에서 B로 가는 방법 중 최단 A → B
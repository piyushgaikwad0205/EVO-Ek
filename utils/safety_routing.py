import heapq
from typing import List, Tuple, Dict

# Example node structure: {'lat': float, 'lon': float, 'safety_score': float}

def dijkstra_safety(nodes: List[Dict], edges: List[Tuple[int, int, float]], start_idx: int, end_idx: int):
    # nodes: list of dicts with lat, lon, safety_score
    # edges: list of (from_idx, to_idx, distance)
    # start_idx, end_idx: indices in nodes
    n = len(nodes)
    dist = [float('inf')] * n
    prev = [None] * n
    dist[start_idx] = 0
    heap = [(0, start_idx)]
    while heap:
        curr_dist, u = heapq.heappop(heap)
        if u == end_idx:
            break
        for v, w in [(to, weight) for (frm, to, weight) in edges if frm == u]:
            # Safety penalty: add (1 - safety_score) * penalty_factor
            penalty = (1 - nodes[v]['safety_score']) * 10
            alt = curr_dist + w + penalty
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
                heapq.heappush(heap, (alt, v))
    # Reconstruct path
    path = []
    u = end_idx
    while u is not None:
        path.append(u)
        u = prev[u]
    path.reverse()
    return path, dist[end_idx]

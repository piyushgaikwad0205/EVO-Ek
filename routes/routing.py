
from fastapi import APIRouter
from db.database import get_hazards
from utils.safety_routing import dijkstra_safety
from typing import List

routing_router = APIRouter()

@routing_router.post("/route")
def calculate_route(start_lat: float, start_lon: float, end_lat: float, end_lon: float):
    hazards = get_hazards()
    # Build nodes: start, end, hazards
    nodes = [
        {"lat": start_lat, "lon": start_lon, "safety_score": 1.0},
        {"lat": end_lat, "lon": end_lon, "safety_score": 1.0}
    ]
    for h in hazards:
        nodes.append({
            "lat": h["latitude"],
            "lon": h["longitude"],
            "safety_score": h.get("safety_score", 1.0)
        })
    # Build edges: connect all nodes (for demo, real app should use road network)
    edges = []
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            if i != j:
                dist = ((nodes[i]["lat"] - nodes[j]["lat"]) ** 2 + (nodes[i]["lon"] - nodes[j]["lon"]) ** 2) ** 0.5
                edges.append((i, j, dist))
    # Run Dijkstra
    path, total_cost = dijkstra_safety(nodes, edges, 0, 1)
    route = [{"lat": nodes[i]["lat"], "lon": nodes[i]["lon"], "safety_score": nodes[i]["safety_score"]} for i in path]
    return {
        "start": {"lat": start_lat, "lon": start_lon},
        "end": {"lat": end_lat, "lon": end_lon},
        "route": route,
        "total_cost": total_cost
    }

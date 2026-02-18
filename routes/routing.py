
from fastapi import APIRouter
from db.database import get_hazards
from utils.safety_routing import dijkstra_safety
from utils.models_loader import ai_model
from typing import List
import math

routing_router = APIRouter()

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two coordinates in km"""
    R = 6371  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    return R * c

@routing_router.post("/route")
def calculate_route(start_lat: float, start_lon: float, end_lat: float, end_lon: float):
    """
    Calculate Safety-First route using AI models
    Returns route with waypoints, safety scores, and risk level
    """
    hazards = get_hazards()
    
    # Build nodes: start, end, and waypoints
    nodes = [
        {"lat": start_lat, "lon": start_lon, "safety_score": 1.0, "type": "start"},
        {"lat": end_lat, "lon": end_lon, "safety_score": 1.0, "type": "end"}
    ]
    
    # Add intermediate waypoints between start and end
    waypoints = generate_waypoints(start_lat, start_lon, end_lat, end_lon, hazards)
    for wp in waypoints:
        nodes.append(wp)
    
    # Calculate safety scores for all waypoints using AI models
    for i, node in enumerate(nodes):
        if node["type"] not in ["start", "end"]:
            # Get nearby hazards for context
            nearby = [h for h in hazards 
                     if abs(h.get('latitude', 0) - node['lat']) < 0.1 
                     and abs(h.get('longitude', 0) - node['lon']) < 0.1]
            
            hazard_type = nearby[0]['hazard_type'] if nearby else 'unknown'
            
            # AI-based safety scoring
            safety_score = ai_model.score_location(
                node['lat'], 
                node['lon'], 
                hazard_type, 
                len(nearby)
            )
            nodes[i]['safety_score'] = safety_score
    
    # Build edges: connect nearby waypoints
    edges = []
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            if i != j:
                dist = haversine_distance(nodes[i]["lat"], nodes[i]["lon"], 
                                         nodes[j]["lat"], nodes[j]["lon"])
                edges.append((i, j, dist))
    
    # Calculate safety-first route using Dijkstra
    path, total_cost = dijkstra_safety(nodes, edges, 0, 1)
    
    # Build response with detailed route information
    route = [
        {
            "lat": nodes[i]["lat"], 
            "lon": nodes[i]["lon"], 
            "safety_score": nodes[i]["safety_score"],
            "risk_level": ai_model._get_risk_level(nodes[i]["safety_score"])
        } 
        for i in path
    ]
    
    # Analyze overall route safety
    avg_safety = sum(r['safety_score'] for r in route) / len(route) if route else 0.5
    
    return {
        "start": {"lat": start_lat, "lon": start_lon},
        "end": {"lat": end_lat, "lon": end_lon},
        "route": route,
        "total_distance_km": total_cost,
        "route_safety_score": avg_safety,
        "overall_risk_level": ai_model._get_risk_level(avg_safety),
        "waypoint_count": len(route),
        "hazard_count": len(hazards)
    }

def generate_waypoints(start_lat, start_lon, end_lat, end_lon, hazards, num_points=5):
    """Generate intermediate waypoints between start and end"""
    waypoints = []
    
    # Linear interpolation for intermediate points
    for i in range(1, num_points):
        fraction = i / num_points
        lat = start_lat + (end_lat - start_lat) * fraction
        lon = start_lon + (end_lon - start_lon) * fraction
        
        # Nudge away from nearby hazards
        for hazard in hazards:
            h_lat = hazard.get('latitude', 0)
            h_lon = hazard.get('longitude', 0)
            distance = haversine_distance(lat, lon, h_lat, h_lon)
            
            if distance < 1:  # Less than 1km away
                # Move waypoint slightly away from hazard
                angle = math.atan2(lat - h_lat, lon - h_lon)
                lat += 0.01 * math.cos(angle)
                lon += 0.01 * math.sin(angle)
        
        waypoints.append({
            "lat": lat,
            "lon": lon,
            "safety_score": 0.5,
            "type": "waypoint"
        })
    
    return waypoints

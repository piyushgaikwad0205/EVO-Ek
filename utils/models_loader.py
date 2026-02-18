# models_loader.py
# AI Models for Safety Scoring and Route Optimization

import os
import numpy as np

try:
    import torch
    import torch.nn as nn
except ImportError:
    torch = None

try:
    import tensorflow as tf
except ImportError:
    tf = None

class SafetyAIModel:
    """AI Model for comprehensive location safety scoring"""
    
    def __init__(self):
        try:
            self.model1 = self.load_model1()
            self.model2 = self.load_model2()
        except Exception as e:
            print(f"Warning: Error loading models: {e}")
            self.model1 = None
            self.model2 = None
        
        self.hazard_weights = {
            'no streetlight': 0.3,      # High risk at night
            'unsafe area': 0.5,         # Very high risk
            'stray animals': 0.2        # Moderate risk
        }
    
    def load_model1(self):
        """Load model 1 for spatial risk analysis (PyTorch)"""
        try:
            model_path = os.path.join(os.path.dirname(__file__), 'model1.pt')
            if torch and os.path.exists(model_path):
                return torch.load(model_path)
        except Exception as e:
            print(f"Model1 loading failed: {e}")
        return None
    
    def load_model2(self):
        """Load model 2 for temporal/contextual analysis (TensorFlow)"""
        try:
            model_path = os.path.join(os.path.dirname(__file__), 'model2.h5')
            if tf and os.path.exists(model_path):
                return tf.keras.models.load_model(model_path)
        except Exception as e:
            print(f"Model2 loading failed: {e}")
        return None
    
    def score_location(self, latitude, longitude, hazard_type, nearby_hazards_count=0):
        """
        Comprehensive AI-based location safety scoring
        Returns: safety_score (0.0 = dangerous, 1.0 = very safe)
        """
        try:
            # Normalize coordinates to [-1, 1] range for neural networks
            lat_norm = (latitude % 90) / 90.0
            lon_norm = (longitude % 180) / 180.0
            
            # Get base hazard weight
            hazard_weight = self.hazard_weights.get(hazard_type, 0.3)
            
            # Model 1: Spatial risk analysis
            spatial_score = self._model1_inference(lat_norm, lon_norm)
            
            # Model 2: Temporal/contextual analysis
            context_score = self._model2_inference(hazard_type, nearby_hazards_count)
            
            # Combine scores: weighted average
            combined_score = (spatial_score * 0.4 + context_score * 0.4 + (1 - hazard_weight) * 0.2)
            
            # Penalty for nearby hazards
            hazard_penalty = min(nearby_hazards_count * 0.05, 0.3)
            final_score = max(0.0, min(1.0, combined_score - hazard_penalty))
            
            return final_score
        except Exception as e:
            print(f"Error scoring location: {e}")
            return 0.5
    
    def _model1_inference(self, lat_norm, lon_norm):
        """Spatial analysis using Model 1"""
        if self.model1:
            try:
                # Simulate model inference
                input_data = torch.tensor([[lat_norm, lon_norm]], dtype=torch.float32)
                with torch.no_grad():
                    # Placeholder for actual model inference
                    output = 0.5 + (lat_norm * 0.3) + (lon_norm * 0.2)
                return float(output)
            except Exception as e:
                print(f"Model1 inference error: {e}")
        
        # Fallback: simple distance-based scoring
        return 0.5 + (lat_norm * 0.25) + (lon_norm * 0.25)
    
    def _model2_inference(self, hazard_type, nearby_count):
        """Contextual analysis using Model 2"""
        if self.model2:
            try:
                # Simulate model inference
                hazard_idx = list(self.hazard_weights.keys()).index(hazard_type) if hazard_type in self.hazard_weights else 0
                input_data = np.array([[hazard_idx, nearby_count]], dtype=np.float32)
                # Placeholder for actual model inference
                output = 0.7 - (nearby_count * 0.1)
                return float(output)
            except Exception as e:
                print(f"Model2 inference error: {e}")
        
        # Fallback: simple contextual scoring
        return 0.7 - (nearby_count * 0.1)
    
    def score_route(self, route_points, hazards_data):
        """
        Score an entire route using AI models
        Returns: route_safety_score and detailed waypoint scores
        """
        waypoint_scores = []
        
        try:
            for point in route_points:
                # Count nearby hazards
                nearby = sum(1 for h in hazards_data 
                            if abs(h.get('latitude', 0) - point.get('lat', 0)) < 0.05 
                            and abs(h.get('longitude', 0) - point.get('lon', 0)) < 0.05)
                
                # Get hazard type if nearby
                nearby_hazard = next((h.get('hazard_type', 'unknown') for h in hazards_data 
                                     if abs(h.get('latitude', 0) - point.get('lat', 0)) < 0.05 
                                     and abs(h.get('longitude', 0) - point.get('lon', 0)) < 0.05), 
                                    'unknown')
                
                score = self.score_location(point['lat'], point['lon'], nearby_hazard, nearby)
                waypoint_scores.append({
                    'lat': point['lat'],
                    'lon': point['lon'],
                    'safety_score': score,
                    'nearby_hazards': nearby
                })
            
            # Calculate route average safety
            avg_safety = np.mean([s['safety_score'] for s in waypoint_scores]) if waypoint_scores else 0.5
            
            return {
                'route_safety_score': float(avg_safety),
                'waypoint_scores': waypoint_scores,
                'risk_level': self._get_risk_level(avg_safety)
            }
        except Exception as e:
            print(f"Error scoring route: {e}")
            return {
                'route_safety_score': 0.5,
                'waypoint_scores': [],
                'risk_level': 'ERROR'
            }
    
    def _get_risk_level(self, safety_score):
        """Classify risk level based on safety score"""
        if safety_score >= 0.8:
            return 'VERY SAFE'
        elif safety_score >= 0.6:
            return 'SAFE'
        elif safety_score >= 0.4:
            return 'MODERATE RISK'
        else:
            return 'HIGH RISK'

# Initialize AI Model Manager
ai_model = SafetyAIModel()


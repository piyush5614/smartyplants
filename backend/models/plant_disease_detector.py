"""
AI/ML module for plant disease detection.
Uses a pre-trained model or custom model for identifying plant diseases.
"""

import numpy as np
from pathlib import Path


class PlantDiseaseDetector:
    """
    Main class for plant disease detection using computer vision.
    Handles model loading, image analysis, and disease classification.
    """
    
    # Disease database with characteristics and severity
    DISEASE_DATABASE = {
        'healthy': {
            'severity': 'none',
            'common_causes': [],
            'description': 'Plant appears healthy with no visible signs of disease'
        },
        'leaf_spot': {
            'severity': 'moderate',
            'common_causes': ['Fungal infection', 'Bacterial infection', 'Poor air circulation'],
            'description': 'Circular or irregular brown/black spots on leaves'
        },
        'powdery_mildew': {
            'severity': 'moderate',
            'common_causes': ['Fungal infection', 'High humidity', 'Poor air flow'],
            'description': 'White powdery coating on leaves and stems'
        },
        'rust': {
            'severity': 'moderate',
            'common_causes': ['Fungal infection', 'High humidity', 'Wet conditions'],
            'description': 'Rust-colored pustules on leaf underside'
        },
        'blight': {
            'severity': 'severe',
            'common_causes': ['Fungal infection', 'Bacterial infection', 'Wet weather'],
            'description': 'Large dark patches on leaves causing rapid leaf death'
        },
        'yellowing': {
            'severity': 'mild',
            'common_causes': ['Nutrient deficiency', 'Poor drainage', 'Overwatering'],
            'description': 'Leaves turning yellow, often starting from older leaves'
        },
        'wilting': {
            'severity': 'severe',
            'common_causes': ['Underwatering', 'Root rot', 'Wilt diseases'],
            'description': 'Plants drooping and losing turgor despite moisture'
        },
        'pest_damage': {
            'severity': 'moderate',
            'common_causes': ['Insect infestation', 'Mites', 'Aphids'],
            'description': 'Holes, discoloration, or abnormal leaf damage'
        }
    }
    
    def __init__(self):
        """Initialize the disease detector."""
        self.model = None
        self.is_loaded = False
        self._load_model()
    
    def _load_model(self):
        """Load the pre-trained model for disease detection."""
        try:
            # In production, load actual TensorFlow/Keras model
            # For now, we'll use a rule-based approach for demonstration
            self.is_loaded = True
        except Exception as e:
            raise Exception(f"Failed to load model: {str(e)}")
    
    def detect_disease(self, image_array: np.ndarray, confidence_threshold: float = 0.7) -> dict:
        """
        Detect plant disease in an image.
        
        Args:
            image_array: numpy array of image data
            confidence_threshold: minimum confidence score for prediction
            
        Returns:
            Dictionary with disease detection results
        """
        if not self.is_loaded:
            raise RuntimeError("Model not loaded")
        
        # Validate image
        if image_array is None or image_array.size == 0:
            return self._format_error_response("Invalid image provided")
        
        try:
            # Extract visual features
            features = self._extract_features(image_array)
            
            # Analyze features and detect disease
            predictions = self._classify_disease(features)
            
            # Filter by confidence threshold
            filtered_predictions = [
                p for p in predictions 
                if p['confidence'] >= confidence_threshold
            ]
            
            if not filtered_predictions:
                filtered_predictions = [predictions[0]]  # Return highest confidence
            
            return {
                'success': True,
                'predictions': filtered_predictions,
                'primary_disease': filtered_predictions[0],
                'feature_analysis': features
            }
            
        except Exception as e:
            return self._format_error_response(f"Detection failed: {str(e)}")
    
    def _extract_features(self, image_array: np.ndarray) -> dict:
        """
        Extract visual features from image.
        
        Args:
            image_array: numpy array of image
            
        Returns:
            Dictionary of extracted features
        """
        # Convert to grayscale for analysis
        if len(image_array.shape) == 3:
            gray = np.mean(image_array, axis=2)
        else:
            gray = image_array
        
        features = {
            'color_variance': float(np.var(image_array)),
            'brightness': float(np.mean(gray)),
            'contrast': float(np.std(image_array)),
            'greenness': self._calculate_greenness(image_array) if len(image_array.shape) == 3 else 0,
            'edge_density': self._calculate_edge_density(gray),
            'damaged_pixels_ratio': self._estimate_damage(image_array)
        }
        
        return features
    
    def _calculate_greenness(self, image_array: np.ndarray) -> float:
        """Calculate the greenness component of the image."""
        if len(image_array.shape) < 3:
            return 0.0
        
        # Assuming RGB format (or BGR)
        green_channel = image_array[:, :, 1]
        red_channel = image_array[:, :, 0]
        blue_channel = image_array[:, :, 2]
        
        # Simple greenness metric
        greenness = np.mean(green_channel) / (np.mean(red_channel) + np.mean(blue_channel) + 1e-5)
        return float(greenness)
    
    def _calculate_edge_density(self, gray_image: np.ndarray) -> float:
        """Calculate edge density in image (indicator of texture/disease)."""
        # Simple edge detection using gradients
        if gray_image.shape[0] < 2 or gray_image.shape[1] < 2:
            return 0.0
        
        gx = np.abs(np.diff(gray_image, axis=0)).mean()
        gy = np.abs(np.diff(gray_image, axis=1)).mean()
        
        return float((gx + gy) / 2.0)
    
    def _estimate_damage(self, image_array: np.ndarray) -> float:
        """Estimate ratio of damaged pixels in image."""
        if image_array.size == 0:
            return 0.0
        
        # Damaged areas typically have extreme colors
        # This is a simplified heuristic
        std_dev = np.std(image_array)
        damage_ratio = min(std_dev / 255.0, 1.0)
        
        return float(damage_ratio)
    
    def _classify_disease(self, features: dict) -> list:
        """
        Classify disease based on extracted features.
        Uses rule-based classification for demonstration.
        
        Args:
            features: Dictionary of extracted features
            
        Returns:
            List of predictions with confidence scores
        """
        predictions = []
        
        # Rule-based disease classification
        scores = self._calculate_disease_scores(features)
        
        # Sort by confidence
        sorted_diseases = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        for disease_name, confidence in sorted_diseases[:5]:
            disease_info = self.DISEASE_DATABASE.get(disease_name, {})
            predictions.append({
                'disease': disease_name,
                'confidence': confidence,
                'severity': disease_info.get('severity', 'unknown'),
                'description': disease_info.get('description', ''),
                'common_causes': disease_info.get('common_causes', [])
            })
        
        return predictions
    
    def _calculate_disease_scores(self, features: dict) -> dict:
        """Calculate confidence scores for each disease based on features."""
        scores = {}
        
        greenness = features.get('greenness', 1.0)
        edge_density = features.get('edge_density', 0.0)
        damage_ratio = features.get('damaged_pixels_ratio', 0.0)
        brightness = features.get('brightness', 128.0)
        
        # Healthy plant: high greenness, low edge density
        scores['healthy'] = max(0, min(greenness, 1.0) * (1 - edge_density * 0.5))
        
        # Leaf spot: moderate greenness, some edge density
        scores['leaf_spot'] = max(0, (1 - greenness) * 0.3 + edge_density * 0.5 + damage_ratio * 0.2)
        
        # Powdery mildew: reduced greenness, high edge density
        scores['powdery_mildew'] = max(0, (1 - greenness) * 0.4 + edge_density * 0.6)
        
        # Rust: similar to leaf spot but with color variance
        scores['rust'] = max(0, (1 - greenness) * 0.35 + edge_density * 0.45 + damage_ratio * 0.2)
        
        # Blight: severe damage, very low greenness
        scores['blight'] = max(0, (1 - greenness) * 0.7 + damage_ratio * 0.6)
        
        # Yellowing: low greenness, intact structure
        scores['yellowing'] = max(0, (1 - greenness) * 0.5 * (1 - edge_density))
        
        # Wilting: brightness variation
        scores['wilting'] = max(0, abs(brightness - 128) / 128 * 0.4)
        
        # Pest damage: high edge density, multiple spots
        scores['pest_damage'] = max(0, edge_density * 0.7 + damage_ratio * 0.3)
        
        # Normalize scores to 0-1 range
        total = sum(scores.values())
        if total > 0:
            scores = {k: v / total for k, v in scores.items()}
        
        return scores
    
    def _format_error_response(self, error_message: str) -> dict:
        """Format error response."""
        return {
            'success': False,
            'error': error_message,
            'predictions': []
        }

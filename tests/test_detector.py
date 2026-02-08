"""Unit tests for plant disease detector."""

import unittest
import numpy as np
from backend.models.plant_disease_detector import PlantDiseaseDetector


class TestPlantDiseaseDetector(unittest.TestCase):
    """Test cases for PlantDiseaseDetector."""

    def setUp(self):
        """Set up test fixtures."""
        self.detector = PlantDiseaseDetector()

    def test_detector_initialization(self):
        """Test detector initializes correctly."""
        self.assertTrue(self.detector.is_loaded)

    def test_detect_disease_with_valid_image(self):
        """Test disease detection with valid image array."""
        # Create a dummy image array
        image_array = np.random.rand(224, 224, 3)
        
        result = self.detector.detect_disease(image_array)
        
        self.assertIsNotNone(result)
        self.assertIn('success', result)
        self.assertTrue(result['success'])
        self.assertIn('predictions', result)
        self.assertTrue(len(result['predictions']) > 0)

    def test_detect_disease_with_invalid_image(self):
        """Test disease detection with invalid image."""
        result = self.detector.detect_disease(None)
        
        self.assertFalse(result['success'])
        self.assertIn('error', result)

    def test_confidence_threshold(self):
        """Test confidence threshold filtering."""
        image_array = np.random.rand(224, 224, 3)
        
        result_low = self.detector.detect_disease(image_array, confidence_threshold=0.3)
        result_high = self.detector.detect_disease(image_array, confidence_threshold=0.9)
        
        # High threshold should be more selective
        self.assertTrue(len(result_low['predictions']) >= len(result_high['predictions']))

    def test_disease_database(self):
        """Test disease database contains expected diseases."""
        expected_diseases = [
            'healthy', 'leaf_spot', 'powdery_mildew', 'rust', 
            'blight', 'yellowing', 'wilting', 'pest_damage'
        ]
        
        for disease in expected_diseases:
            self.assertIn(disease, self.detector.DISEASE_DATABASE)

    def test_feature_extraction(self):
        """Test feature extraction from image."""
        image_array = np.random.rand(224, 224, 3)
        features = self.detector._extract_features(image_array)
        
        self.assertIn('color_variance', features)
        self.assertIn('brightness', features)
        self.assertIn('contrast', features)
        self.assertIn('edge_density', features)
        self.assertIn('damaged_pixels_ratio', features)


if __name__ == '__main__':
    unittest.main()

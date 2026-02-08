"""
Logic Engine for Smart Plant Health Assistant.
Interprets AI analysis and generates conditional suggestions.
Pure IF-ELSE logic - NO API calls, NO UI code, NO authentication.
"""

from typing import Dict, List, Optional


class LogicEngine:
    """
    Service for interpreting AI analysis and generating smart suggestions.
    Responsibilities: IF-ELSE conditions, suggestions, risk assessment.
    Focus: Pure logic only - NO external calls, NO UI code.
    """
    
    # Disease categories
    FUNGAL_DISEASES = [
        'powdery mildew',
        'leaf spot',
        'rust',
        'blight',
        'anthracnose',
        'damping off',
        'root rot',
        'mildew'
    ]
    
    BACTERIAL_DISEASES = [
        'bacterial leaf spot',
        'bacterial blight',
        'crown gall',
        'bacterial wilt',
        'fire blight'
    ]
    
    VIRAL_DISEASES = [
        'mosaic virus',
        'leaf curl virus',
        'viral infection',
        'virus disease'
    ]
    
    ENVIRONMENTAL_STRESSES = [
        'water stress',
        'drought stress',
        'overwatering',
        'nutrient deficiency',
        'nitrogen deficiency',
        'phosphorus deficiency',
        'potassium deficiency',
        'chlorosis',
        'yellowing',
        'sunburn',
        'cold damage',
        'heat stress'
    ]
    
    # Confidence thresholds
    HIGH_CONFIDENCE_THRESHOLD = 80.0
    MEDIUM_CONFIDENCE_THRESHOLD = 50.0
    LOW_CONFIDENCE_THRESHOLD = 0.0
    
    # Health score ranges
    HEALTH_CRITICAL_THRESHOLD = 20.0
    HEALTH_POOR_THRESHOLD = 40.0
    HEALTH_FAIR_THRESHOLD = 60.0
    HEALTH_GOOD_THRESHOLD = 80.0
    
    def __init__(self):
        """Initialize Logic Engine with default parameters."""
        self.low_confidence_threshold = self.MEDIUM_CONFIDENCE_THRESHOLD
        self.urgent_action_threshold = self.HEALTH_CRITICAL_THRESHOLD
    
    def process_analysis(self, ai_analysis: Dict) -> Dict:
        """
        Process AI analysis and generate actionable insights.
        
        Args:
            ai_analysis: Dictionary containing AI analysis results
        
        Returns:
            Processed analysis with conditions and suggestions
        """
        if not ai_analysis:
            return self._create_error_response("Empty analysis")
        
        # Extract key metrics
        diagnosis = ai_analysis.get('diagnosis', '').lower()
        confidence = ai_analysis.get('confidence', 0.0)
        health_score = ai_analysis.get('health_score', 50.0)
        severity = ai_analysis.get('severity', 'unknown').lower()
        raw_analysis = ai_analysis.get('raw_analysis', '')
        
        # Initialize result
        result = {
            'original_analysis': diagnosis,
            'confidence': confidence,
            'health_score': health_score,
            'severity': severity,
            'conditions': [],
            'suggestions': [],
            'urgent_actions': [],
            'disease_category': None,
            'risk_assessment': None,
            'follow_up': None
        }
        
        # Apply conditional logic
        result['conditions'] = self._evaluate_conditions(
            diagnosis, confidence, health_score, severity, raw_analysis
        )
        
        result['disease_category'] = self._classify_disease(diagnosis)
        result['suggestions'] = self._generate_suggestions(
            diagnosis, confidence, health_score, severity, result['disease_category']
        )
        result['urgent_actions'] = self._generate_urgent_actions(
            health_score, severity, result['disease_category']
        )
        result['risk_assessment'] = self._assess_risk(
            diagnosis, health_score, severity
        )
        result['follow_up'] = self._determine_followup(confidence, health_score)
        
        return result
    
    def _evaluate_conditions(
        self,
        diagnosis: str,
        confidence: float,
        health_score: float,
        severity: str,
        raw_analysis: str
    ) -> List[str]:
        """
        Evaluate conditions based on analysis metrics.
        
        Args:
            diagnosis: Diagnosed condition
            confidence: Confidence percentage (0-100)
            health_score: Health score (0-100)
            severity: Disease severity (mild, moderate, severe)
            raw_analysis: Raw AI analysis text
        
        Returns:
            List of detected conditions
        """
        conditions = []
        
        # CONDITION 1: Low confidence detection
        if confidence < self.low_confidence_threshold:
            conditions.append("LOW_CONFIDENCE_DIAGNOSIS")
        
        # CONDITION 2: Very low confidence (ambiguous diagnosis)
        if confidence < self.MEDIUM_CONFIDENCE_THRESHOLD:
            conditions.append("AMBIGUOUS_DIAGNOSIS")
        
        # CONDITION 3: High confidence
        if confidence >= self.HIGH_CONFIDENCE_THRESHOLD:
            conditions.append("HIGH_CONFIDENCE_DIAGNOSIS")
        
        # CONDITION 4: Critical health status
        if health_score <= self.HEALTH_CRITICAL_THRESHOLD:
            conditions.append("CRITICAL_PLANT_HEALTH")
        
        # CONDITION 5: Poor health status
        if health_score <= self.HEALTH_POOR_THRESHOLD:
            conditions.append("POOR_PLANT_HEALTH")
        
        # CONDITION 6: Fair health status
        if health_score <= self.HEALTH_FAIR_THRESHOLD:
            conditions.append("FAIR_PLANT_HEALTH")
        
        # CONDITION 7: Good health status
        if health_score >= self.HEALTH_GOOD_THRESHOLD:
            conditions.append("GOOD_PLANT_HEALTH")
        
        # CONDITION 8: Fungal disease detected
        if self._is_fungal_disease(diagnosis):
            conditions.append("FUNGAL_DISEASE_DETECTED")
        
        # CONDITION 9: Bacterial disease detected
        if self._is_bacterial_disease(diagnosis):
            conditions.append("BACTERIAL_DISEASE_DETECTED")
        
        # CONDITION 10: Viral disease detected
        if self._is_viral_disease(diagnosis):
            conditions.append("VIRAL_DISEASE_DETECTED")
        
        # CONDITION 11: Water stress detected
        if self._is_water_stress(diagnosis, raw_analysis):
            conditions.append("WATER_STRESS_DETECTED")
        
        # CONDITION 12: Nutrient deficiency detected
        if self._is_nutrient_deficiency(diagnosis, raw_analysis):
            conditions.append("NUTRIENT_DEFICIENCY_DETECTED")
        
        # CONDITION 13: Severe disease
        if severity == 'severe':
            conditions.append("SEVERE_DISEASE")
        
        # CONDITION 14: Moderate disease
        if severity == 'moderate':
            conditions.append("MODERATE_DISEASE")
        
        # CONDITION 15: Mild disease
        if severity == 'mild':
            conditions.append("MILD_DISEASE")
        
        # CONDITION 16: Emergency intervention needed
        if health_score <= self.HEALTH_CRITICAL_THRESHOLD and severity == 'severe':
            conditions.append("EMERGENCY_INTERVENTION_NEEDED")
        
        # CONDITION 17: Environmental stress (non-disease)
        if self._is_environmental_stress(diagnosis) and not self._is_disease(diagnosis):
            conditions.append("ENVIRONMENTAL_STRESS_ONLY")
        
        # CONDITION 18: Healthy plant
        if health_score >= self.HEALTH_GOOD_THRESHOLD and confidence >= self.MEDIUM_CONFIDENCE_THRESHOLD:
            conditions.append("PLANT_APPEARS_HEALTHY")
        
        return conditions
    
    def _classify_disease(self, diagnosis: str) -> Optional[str]:
        """
        Classify disease into category.
        
        Args:
            diagnosis: Disease diagnosis text
        
        Returns:
            Disease category or None
        """
        diagnosis_lower = diagnosis.lower()
        
        # Check fungal
        if self._is_fungal_disease(diagnosis_lower):
            return 'FUNGAL'
        
        # Check bacterial
        if self._is_bacterial_disease(diagnosis_lower):
            return 'BACTERIAL'
        
        # Check viral
        if self._is_viral_disease(diagnosis_lower):
            return 'VIRAL'
        
        # Check environmental
        if self._is_environmental_stress(diagnosis_lower):
            return 'ENVIRONMENTAL'
        
        # Check pest damage
        if 'pest' in diagnosis_lower or 'insect' in diagnosis_lower:
            return 'PEST_DAMAGE'
        
        # Unknown/healthy
        if 'healthy' in diagnosis_lower or 'no disease' in diagnosis_lower:
            return 'HEALTHY'
        
        return 'UNKNOWN'
    
    def _generate_suggestions(
        self,
        diagnosis: str,
        confidence: float,
        health_score: float,
        severity: str,
        disease_category: Optional[str]
    ) -> List[Dict]:
        """
        Generate actionable suggestions based on analysis.
        
        Args:
            diagnosis: Disease diagnosis
            confidence: Confidence percentage
            health_score: Plant health score
            severity: Disease severity
            disease_category: Classified disease category
        
        Returns:
            List of suggestion dictionaries
        """
        suggestions = []
        
        # SUGGESTION 1: Fungal disease treatment
        if disease_category == 'FUNGAL':
            if severity == 'severe':
                suggestions.append({
                    'type': 'FUNGAL_DISEASE_TREATMENT',
                    'priority': 'URGENT',
                    'action': 'Apply fungicide immediately',
                    'details': [
                        'Use broad-spectrum fungicide (e.g., sulfur, copper)',
                        'Apply every 7-10 days until improvement',
                        'Remove affected leaves',
                        'Improve air circulation',
                        'Reduce leaf wetness (avoid overhead watering)'
                    ]
                })
            elif severity == 'moderate':
                suggestions.append({
                    'type': 'FUNGAL_DISEASE_TREATMENT',
                    'priority': 'HIGH',
                    'action': 'Treat fungal infection',
                    'details': [
                        'Apply fungicide spray',
                        'Repeat treatment every 10-14 days',
                        'Remove moderately affected leaves',
                        'Improve air circulation and reduce humidity'
                    ]
                })
            else:  # mild
                suggestions.append({
                    'type': 'FUNGAL_DISEASE_TREATMENT',
                    'priority': 'MEDIUM',
                    'action': 'Monitor and treat early fungal signs',
                    'details': [
                        'Apply preventative fungicide',
                        'Remove affected leaves',
                        'Monitor closely for spread'
                    ]
                })
        
        # SUGGESTION 2: Bacterial disease treatment
        if disease_category == 'BACTERIAL':
            if severity == 'severe':
                suggestions.append({
                    'type': 'BACTERIAL_DISEASE_TREATMENT',
                    'priority': 'URGENT',
                    'action': 'Address bacterial infection urgently',
                    'details': [
                        'Remove severely affected plant parts',
                        'Apply copper-based bactericide',
                        'Sterilize tools between cuts',
                        'Avoid watering foliage',
                        'Consider plant removal if severely infected'
                    ]
                })
            else:
                suggestions.append({
                    'type': 'BACTERIAL_DISEASE_TREATMENT',
                    'priority': 'HIGH',
                    'action': 'Treat bacterial infection',
                    'details': [
                        'Apply copper spray',
                        'Remove infected plant material',
                        'Prevent wetting of leaves',
                        'Improve drainage'
                    ]
                })
        
        # SUGGESTION 3: Viral disease treatment
        if disease_category == 'VIRAL':
            suggestions.append({
                'type': 'VIRAL_DISEASE_TREATMENT',
                'priority': 'URGENT',
                'action': 'Manage viral infection',
                'details': [
                    'Remove entire affected plant (no cure for viruses)',
                    'Control insect vectors (aphids, whiteflies)',
                    'Disinfect tools to prevent spread',
                    'No chemical treatment available',
                    'Focus on prevention for other plants'
                ]
            })
        
        # SUGGESTION 4: Water stress
        if 'WATER_STRESS_DETECTED' in [c for c in self._evaluate_conditions(
            diagnosis, confidence, health_score, severity, diagnosis
        )]:
            if 'drought' in diagnosis.lower() or 'dry' in diagnosis.lower():
                suggestions.append({
                    'type': 'WATER_MANAGEMENT',
                    'priority': 'HIGH',
                    'action': 'Address drought stress',
                    'details': [
                        'Water deeply and thoroughly',
                        'Water less frequently but more thoroughly',
                        'Add mulch to retain moisture',
                        'Water during early morning or evening',
                        'Check soil moisture regularly (should be moist not wet)'
                    ]
                })
            else:  # overwatering
                suggestions.append({
                    'type': 'WATER_MANAGEMENT',
                    'priority': 'HIGH',
                    'action': 'Reduce watering',
                    'details': [
                        'Allow soil to dry between waterings',
                        'Improve drainage (repot if needed)',
                        'Reduce watering frequency',
                        'Ensure pot has drainage holes',
                        'Check for root rot'
                    ]
                })
        
        # SUGGESTION 5: Nutrient deficiency
        if 'NUTRIENT_DEFICIENCY_DETECTED' in [c for c in self._evaluate_conditions(
            diagnosis, confidence, health_score, severity, diagnosis
        )]:
            suggestions.append({
                'type': 'NUTRIENT_MANAGEMENT',
                'priority': 'MEDIUM',
                'action': 'Address nutrient deficiency',
                'details': [
                    'Apply balanced fertilizer (NPK 10-10-10)',
                    'Feed every 2-4 weeks during growing season',
                    'Use slow-release fertilizer',
                    'Consider foliar spray for quick recovery',
                    'Repot with fresh soil if last repotted >1 year ago'
                ]
            })
        
        # SUGGESTION 6: Low confidence diagnosis
        if confidence < self.MEDIUM_CONFIDENCE_THRESHOLD:
            suggestions.append({
                'type': 'DIAGNOSIS_CLARIFICATION',
                'priority': 'HIGH',
                'action': 'Get professional confirmation',
                'details': [
                    'Diagnosis is uncertain',
                    'Consult local plant expert or extension service',
                    'Take multiple clear photos from different angles',
                    'Monitor plant closely for symptom development',
                    'Consider waiting to see symptom progression'
                ]
            })
        
        # SUGGESTION 7: Environmental stress
        if disease_category == 'ENVIRONMENTAL':
            suggestions.append({
                'type': 'ENVIRONMENTAL_ADJUSTMENT',
                'priority': 'MEDIUM',
                'action': 'Improve growing conditions',
                'details': [
                    'Review light conditions (6-8 hours for most plants)',
                    'Check temperature (65-75°F optimal for most plants)',
                    'Monitor humidity (40-60% for most plants)',
                    'Ensure adequate air circulation',
                    'Avoid placing near heating/cooling vents'
                ]
            })
        
        # SUGGESTION 8: Pest damage
        if disease_category == 'PEST_DAMAGE':
            suggestions.append({
                'type': 'PEST_MANAGEMENT',
                'priority': 'HIGH',
                'action': 'Control pests',
                'details': [
                    'Inspect regularly for insect presence',
                    'Isolate plant to prevent spread',
                    'Use neem oil or insecticidal soap',
                    'Remove heavily infested leaves',
                    'Repeat treatment weekly until clear'
                ]
            })
        
        # SUGGESTION 9: Preventative maintenance
        if health_score >= self.HEALTH_GOOD_THRESHOLD or disease_category == 'HEALTHY':
            suggestions.append({
                'type': 'PREVENTATIVE_CARE',
                'priority': 'LOW',
                'action': 'Maintain plant health',
                'details': [
                    'Continue regular watering schedule',
                    'Feed monthly during growing season',
                    'Monitor for early disease signs',
                    'Ensure good air circulation',
                    'Clean leaves monthly to improve photosynthesis'
                ]
            })
        
        return suggestions
    
    def _generate_urgent_actions(
        self,
        health_score: float,
        severity: str,
        disease_category: Optional[str]
    ) -> List[str]:
        """
        Generate urgent immediate actions if needed.
        
        Args:
            health_score: Plant health score
            severity: Disease severity
            disease_category: Disease category
        
        Returns:
            List of urgent action strings
        """
        urgent_actions = []
        
        # URGENT ACTION 1: Critical health
        if health_score <= self.HEALTH_CRITICAL_THRESHOLD:
            urgent_actions.append("ISOLATE PLANT: Prevent disease spread to other plants")
        
        # URGENT ACTION 2: Severe disease
        if severity == 'severe':
            urgent_actions.append("TREAT IMMEDIATELY: Disease is advancing rapidly")
        
        # URGENT ACTION 3: Fungal + severe
        if disease_category == 'FUNGAL' and severity == 'severe':
            urgent_actions.append("APPLY FUNGICIDE: Fungal diseases spread quickly")
        
        # URGENT ACTION 4: Viral disease
        if disease_category == 'VIRAL':
            urgent_actions.append("CONSIDER REMOVAL: Viruses cannot be cured, only contained")
        
        # URGENT ACTION 5: Critical + environmental
        if health_score <= self.HEALTH_CRITICAL_THRESHOLD and disease_category == 'ENVIRONMENTAL':
            urgent_actions.append("CHANGE CONDITIONS: Environmental stress is critical")
        
        # URGENT ACTION 6: Pest infestation
        if disease_category == 'PEST_DAMAGE' and severity == 'severe':
            urgent_actions.append("ISOLATE AND TREAT: Pest infestation is severe")
        
        return urgent_actions
    
    def _assess_risk(
        self,
        diagnosis: str,
        health_score: float,
        severity: str
    ) -> Dict:
        """
        Assess plant risk factors.
        
        Args:
            diagnosis: Disease diagnosis
            health_score: Plant health score
            severity: Disease severity
        
        Returns:
            Risk assessment dictionary
        """
        risk_score = 0  # 0-100, higher = riskier
        risk_factors = []
        
        # Factor 1: Low health score
        if health_score <= self.HEALTH_CRITICAL_THRESHOLD:
            risk_score += 40
            risk_factors.append("Critical plant health")
        elif health_score <= self.HEALTH_POOR_THRESHOLD:
            risk_score += 25
            risk_factors.append("Poor plant health")
        
        # Factor 2: Disease severity
        if severity == 'severe':
            risk_score += 30
            risk_factors.append("Severe disease status")
        elif severity == 'moderate':
            risk_score += 15
            risk_factors.append("Moderate disease status")
        
        # Factor 3: Disease type
        if self._is_viral_disease(diagnosis):
            risk_score += 20
            risk_factors.append("Viral disease (incurable)")
        elif self._is_fungal_disease(diagnosis):
            risk_score += 15
            risk_factors.append("Fungal disease (spreads quickly)")
        
        # Factor 4: Spread risk
        if 'ENVIRONMENTAL_STRESS' not in diagnosis.lower():
            # Diseases spread more than environmental stress
            risk_score += 5
        
        # Cap risk score at 100
        risk_score = min(risk_score, 100)
        
        # Determine risk level
        if risk_score >= 75:
            risk_level = 'CRITICAL'
        elif risk_score >= 50:
            risk_level = 'HIGH'
        elif risk_score >= 25:
            risk_level = 'MEDIUM'
        else:
            risk_level = 'LOW'
        
        return {
            'risk_score': risk_score,
            'risk_level': risk_level,
            'risk_factors': risk_factors
        }
    
    def _determine_followup(
        self,
        confidence: float,
        health_score: float
    ) -> Dict:
        """
        Determine follow-up monitoring schedule.
        
        Args:
            confidence: Diagnosis confidence
            health_score: Plant health score
        
        Returns:
            Follow-up plan dictionary
        """
        if health_score <= self.HEALTH_CRITICAL_THRESHOLD:
            # Critical: daily monitoring
            return {
                'schedule': 'DAILY',
                'days': 1,
                'duration_days': 7,
                'reason': 'Plant is in critical condition'
            }
        elif health_score <= self.HEALTH_POOR_THRESHOLD:
            # Poor: every 2-3 days
            return {
                'schedule': 'EVERY_2_3_DAYS',
                'days': 3,
                'duration_days': 14,
                'reason': 'Plant health is poor'
            }
        elif health_score <= self.HEALTH_FAIR_THRESHOLD:
            # Fair: weekly
            return {
                'schedule': 'WEEKLY',
                'days': 7,
                'duration_days': 30,
                'reason': 'Plant health is fair'
            }
        else:
            # Good: every 2 weeks
            return {
                'schedule': 'BI_WEEKLY',
                'days': 14,
                'duration_days': 60,
                'reason': 'Plant appears healthy'
            }
    
    def _is_fungal_disease(self, text: str) -> bool:
        """Check if text indicates fungal disease."""
        return any(disease in text.lower() for disease in self.FUNGAL_DISEASES)
    
    def _is_bacterial_disease(self, text: str) -> bool:
        """Check if text indicates bacterial disease."""
        return any(disease in text.lower() for disease in self.BACTERIAL_DISEASES)
    
    def _is_viral_disease(self, text: str) -> bool:
        """Check if text indicates viral disease."""
        return any(disease in text.lower() for disease in self.VIRAL_DISEASES)
    
    def _is_water_stress(self, diagnosis: str, raw_analysis: str = "") -> bool:
        """Check if water stress is indicated."""
        text = (diagnosis + " " + raw_analysis).lower()
        water_indicators = ['drought', 'water', 'dry', 'wilt', 'overwater']
        return any(indicator in text for indicator in water_indicators)
    
    def _is_nutrient_deficiency(self, diagnosis: str, raw_analysis: str = "") -> bool:
        """Check if nutrient deficiency is indicated."""
        text = (diagnosis + " " + raw_analysis).lower()
        nutrient_indicators = [
            'nutrient', 'nitrogen', 'phosphorus', 'potassium',
            'deficiency', 'chlorosis', 'yellowing', 'pale'
        ]
        return any(indicator in text for indicator in nutrient_indicators)
    
    def _is_environmental_stress(self, text: str) -> bool:
        """Check if environmental stress is indicated."""
        return any(stress in text.lower() for stress in self.ENVIRONMENTAL_STRESSES)
    
    def _is_disease(self, text: str) -> bool:
        """Check if disease (not environmental) is indicated."""
        disease_indicators = [
            'disease', 'infection', 'fungal', 'bacterial', 'viral',
            'blight', 'rust', 'mildew', 'spot', 'rot'
        ]
        return any(indicator in text.lower() for indicator in disease_indicators)
    
    def _create_error_response(self, error_message: str) -> Dict:
        """Create standardized error response."""
        return {
            'original_analysis': error_message,
            'confidence': 0.0,
            'health_score': 50.0,
            'severity': 'unknown',
            'conditions': ['ERROR_PROCESSING_ANALYSIS'],
            'suggestions': [],
            'urgent_actions': [f"Error: {error_message}"],
            'disease_category': None,
            'risk_assessment': {
                'risk_score': 50,
                'risk_level': 'UNKNOWN',
                'risk_factors': [error_message]
            },
            'follow_up': {
                'schedule': 'IMMEDIATE_REVIEW',
                'reason': error_message
            }
        }

"""
Care advisor service.
Provides actionable care advice based on disease detection and analysis.
"""

from typing import Dict, List


class CareAdvisor:
    """
    Service for providing plant care advice.
    Generates practical recommendations based on disease analysis.
    """
    
    # Comprehensive care recommendations database
    CARE_DATABASE = {
        'healthy': {
            'immediate_actions': [
                'Continue regular watering schedule',
                'Maintain current lighting conditions',
                'Keep monitoring for any changes'
            ],
            'preventive_measures': [
                'Maintain good air circulation around the plant',
                'Avoid overcrowding with other plants',
                'Water at the base to keep leaves dry',
                'Remove any dead leaves promptly',
                'Inspect plant weekly for early signs of disease'
            ],
            'watering': {
                'frequency': 'Every 2-3 days',
                'amount': 'Until soil is moist but not waterlogged',
                'tip': 'Water in the morning to allow foliage to dry'
            },
            'fertilizing': {
                'frequency': 'Every 2-4 weeks during growing season',
                'type': 'Balanced fertilizer (NPK 10-10-10)',
                'tip': 'Reduce frequency in winter months'
            },
            'sunlight': {
                'requirement': 'Maintain current light level',
                'tip': 'Most houseplants prefer bright, indirect light'
            }
        },
        'leaf_spot': {
            'immediate_actions': [
                'Remove infected leaves immediately',
                'Isolate plant from others if possible',
                'Stop overhead watering',
                'Apply fungicide spray (neem oil or sulfur)',
                'Improve air circulation with a fan'
            ],
            'treatment': {
                'organic': [
                    'Spray with neem oil every 7-10 days',
                    'Apply baking soda solution (1 tbsp per gallon)',
                    'Use milk spray (1 part milk to 9 parts water)'
                ],
                'chemical': [
                    'Use copper fungicide',
                    'Apply sulfur-based fungicide',
                    'Use systemic fungicide for severe cases'
                ]
            },
            'preventive_measures': [
                'Space plants properly for air flow',
                'Water soil only, avoid wetting leaves',
                'Remove lower leaves (6 inches from soil)',
                'Disinfect pruning tools with 10% bleach',
                'Avoid touching wet leaves'
            ],
            'watering': {
                'frequency': 'Every 2-3 days (let soil surface dry between)',
                'method': 'Water at base only, never spray foliage',
                'tip': 'Water in early morning to minimize leaf wetness'
            }
        },
        'powdery_mildew': {
            'immediate_actions': [
                'Increase air circulation immediately',
                'Lower humidity levels',
                'Spray with fungicide',
                'Remove heavily affected leaves',
                'Avoid crowding plants together'
            ],
            'treatment': {
                'organic': [
                    'Spray with baking soda solution weekly',
                    'Apply milk spray (1:9 ratio)',
                    'Use sulfur dust or spray',
                    'Neem oil application every 7 days'
                ],
                'chemical': [
                    'Use potassium bicarbonate fungicide',
                    'Apply sulfur-based fungicide',
                    'Use commercial powdery mildew spray'
                ]
            },
            'environmental': {
                'temperature': 'Keep between 60-75°F',
                'humidity': 'Maintain below 50%',
                'air_flow': 'Use fan to improve circulation',
                'space': 'Ensure 6-8 inches between plants'
            },
            'preventive_measures': [
                'Never overhead water - use base watering only',
                'Maintain good air circulation',
                'Keep humidity low (use dehumidifier if needed)',
                'Remove infected leaves immediately',
                'Disinfect tools between plants'
            ]
        },
        'rust': {
            'immediate_actions': [
                'Remove infected leaves at the first sign',
                'Improve air circulation',
                'Reduce leaf wetness duration',
                'Apply fungicide spray',
                'Lower humidity levels'
            ],
            'treatment': {
                'organic': [
                    'Spray with sulfur fungicide',
                    'Use neem oil weekly',
                    'Apply copper fungicide'
                ],
                'chemical': [
                    'Use triazole fungicide',
                    'Apply myclobutanil spray',
                    'Use commercial rust treatment'
                ]
            },
            'watering': {
                'method': 'Water at soil level only',
                'timing': 'Early morning to allow any splash to dry',
                'frequency': 'Every 3-4 days depending on soil',
                'tip': 'Avoid wetting foliage completely'
            },
            'preventive_measures': [
                'Space plants with adequate air flow',
                'Avoid overhead irrigation',
                'Remove rust-infected leaves promptly',
                'Clean fallen leaves regularly',
                'Maintain temperature between 60-75°F'
            ]
        },
        'blight': {
            'immediate_actions': [
                'URGENT: Remove all infected parts immediately',
                'Destroy infected leaves (do not compost)',
                'Isolate plant from other plants',
                'Apply heavy fungicide treatment',
                'Consider destroying entire plant if severely affected'
            ],
            'severity_warning': 'This is a serious disease - act quickly!',
            'treatment': {
                'chemical': [
                    'Apply copper fungicide immediately',
                    'Use chlorothalonil fungicide every 7 days',
                    'Apply mancozeb fungicide',
                    'Use professional-grade fungicides'
                ],
                'aggressive': [
                    'Prune all infected branches 12 inches below visible damage',
                    'Remove entire plant if more than 50% affected',
                    'Sterilize tools with bleach solution after each cut'
                ]
            },
            'quarantine': {
                'duration': '2-4 weeks minimum',
                'isolation': 'Keep plant completely separate',
                'warning': 'Highly contagious - do not touch other plants'
            },
            'recovery': {
                'timeline': '4-8 weeks for recovery',
                'success_rate': '50% if caught early, lower if advanced',
                'monitoring': 'Check daily for new symptoms'
            }
        },
        'yellowing': {
            'immediate_actions': [
                'Check soil moisture level',
                'Assess drainage holes',
                'Look for root rot (smell foul odor)',
                'Check nutrient levels in soil'
            ],
            'diagnosis_steps': [
                'If soil is soggy: Reduce watering, improve drainage',
                'If soil is dry: Increase watering frequency',
                'If older leaves only: Normal aging, remove them',
                'If all leaves: Check for nutrient deficiency'
            ],
            'treatment': {
                'overwatering': [
                    'Let soil dry out for 2-3 days',
                    'Repot with fresh soil if root rot present',
                    'Ensure pot has drainage holes',
                    'Water only when soil is dry 2 inches down'
                ],
                'underwatering': [
                    'Water thoroughly until drains from bottom',
                    'Increase frequency to every 2-3 days',
                    'Mist leaves if air is very dry',
                    'Ensure humidity is adequate'
                ],
                'nutrient_deficiency': [
                    'Apply balanced fertilizer (10-10-10)',
                    'Use liquid fertilizer for faster results',
                    'Repeat every 2-3 weeks',
                    'Consider micronutrient deficiency (iron, magnesium)'
                ]
            },
            'watering_guide': {
                'check': 'Stick finger 2 inches into soil',
                'moist': 'Wait 2-3 days before watering',
                'dry': 'Water immediately',
                'frequency': 'Typically every 3-5 days'
            }
        },
        'wilting': {
            'immediate_actions': [
                'Check soil moisture immediately',
                'Feel if soil is dry or soggy',
                'Check for root damage or rot',
                'Provide immediate water or drainage correction'
            ],
            'diagnosis': {
                'dry_soil': [
                    'Water thoroughly immediately',
                    'Ensure soil is completely saturated',
                    'Let drain completely',
                    'Increase watering frequency',
                    'Monitor recovery over 24-48 hours'
                ],
                'wet_soil': [
                    'Do not water further',
                    'Repot in fresh, dry soil',
                    'Check for root rot (black, mushy roots)',
                    'Remove damaged roots with clean tools',
                    'Reduce watering in future'
                ],
                'wilt_disease': [
                    'No cure available for wilt diseases',
                    'Support plant with stake/cage',
                    'Keep well-watered (but not soggy)',
                    'Remove infected parts',
                    'Consider disposal if spreading'
                ]
            },
            'watering': {
                'frequency': 'Keep soil consistently moist',
                'amount': 'Water when top inch is dry',
                'method': 'Slow, deep watering preferred',
                'humidity': 'Mist foliage to reduce stress'
            }
        },
        'pest_damage': {
            'immediate_actions': [
                'Isolate plant from other plants',
                'Inspect undersides of leaves closely',
                'Identify pest type (aphids, mites, scale, etc.)',
                'Apply appropriate treatment',
                'Monitor plant daily'
            ],
            'treatment': {
                'organic': [
                    'Spray with insecticidal soap',
                    'Use neem oil every 7 days for 3 weeks',
                    'Apply horticultural oil',
                    'Manual removal with cotton swab + rubbing alcohol'
                ],
                'chemical': [
                    'Use systemic insecticide',
                    'Apply pyrethrin spray',
                    'Use commercial pest spray per instructions'
                ]
            },
            'application_tips': [
                'Spray both sides of leaves thoroughly',
                'Include stems and soil surface',
                'Repeat treatment every 7-10 days',
                'Wash hands after application',
                'Treat in early morning or evening'
            ],
            'preventive_measures': [
                'Inspect new plants before bringing home',
                'Quarantine new plants for 2 weeks',
                'Keep plant leaves clean with gentle spray',
                'Maintain good humidity (some pests prefer dry)',
                'Regular monitoring - catch early'
            ]
        }
    }
    
    def __init__(self):
        """Initialize care advisor."""
        self.advice_history = {}
    
    def generate_care_plan(self, analysis_result: Dict) -> Dict:
        """
        Generate comprehensive care plan based on analysis.
        
        Args:
            analysis_result: Result from plant analyzer
            
        Returns:
            Detailed care plan with actionable advice
        """
        if not analysis_result.get('success'):
            return {
                'success': False,
                'error': 'Cannot generate care plan from failed analysis'
            }
        
        disease = analysis_result['disease_detection']['primary_disease']
        severity = analysis_result['disease_detection']['severity']
        confidence = analysis_result['disease_detection']['confidence']
        
        # Get base care recommendations
        care_advice = self.CARE_DATABASE.get(
            disease,
            self._get_default_care()
        )
        
        # Adjust advice based on severity
        adjusted_advice = self._adjust_for_severity(care_advice, severity)
        
        # Create comprehensive care plan
        care_plan = {
            'success': True,
            'disease': disease,
            'severity': severity,
            'confidence': confidence,
            'care_plan': adjusted_advice,
            'priority_actions': self._extract_priority_actions(adjusted_advice, severity),
            'timeline': self._generate_timeline(disease, severity),
            'tips': self._get_tips_by_disease(disease),
            'faq': self._get_faq(disease),
            'emergency_contacts': self._get_emergency_info(severity)
        }
        
        return care_plan
    
    def _adjust_for_severity(self, care_advice: Dict, severity: str) -> Dict:
        """Adjust care advice based on disease severity."""
        adjusted = care_advice.copy()
        
        if severity == 'severe':
            adjusted['urgency'] = 'CRITICAL - Act immediately'
            adjusted['timeline'] = '24-48 hours for initial treatment'
            adjusted['monitoring'] = 'Check every 12 hours'
        elif severity == 'moderate':
            adjusted['urgency'] = 'High - Treat within 2-3 days'
            adjusted['timeline'] = '1-2 weeks for significant improvement'
            adjusted['monitoring'] = 'Check every 2-3 days'
        else:
            adjusted['urgency'] = 'Standard - Treat within 1 week'
            adjusted['timeline'] = '2-4 weeks for recovery'
            adjusted['monitoring'] = 'Check weekly'
        
        return adjusted
    
    def _extract_priority_actions(self, care_advice: Dict, severity: str) -> List[str]:
        """Extract top priority actions from care advice."""
        actions = care_advice.get('immediate_actions', []).copy()
        
        if severity == 'severe':
            return actions[:3]  # Top 3 most critical
        elif severity == 'moderate':
            return actions[:5]
        else:
            return actions
    
    def _generate_timeline(self, disease: str, severity: str) -> Dict:
        """Generate treatment timeline."""
        timelines = {
            'immediate': '0-24 hours',
            'short_term': '1-7 days',
            'medium_term': '2-4 weeks',
            'long_term': '1-3 months'
        }
        
        return {
            'assessment': timelines['immediate'],
            'initial_treatment': timelines['immediate'],
            'first_signs_improvement': timelines['short_term'],
            'significant_improvement': timelines['medium_term'],
            'full_recovery': timelines['long_term']
        }
    
    def _get_tips_by_disease(self, disease: str) -> List[str]:
        """Get helpful tips for specific disease."""
        tips_map = {
            'healthy': [
                'Consistency is key - maintain current schedule',
                'Prevention is easier than cure',
                'Regular monitoring prevents problems'
            ],
            'leaf_spot': [
                'Remove infected leaves as soon as possible',
                'Never water from above',
                'Improve spacing between plants'
            ],
            'powdery_mildew': [
                'Humidity is your enemy - keep below 50%',
                'Air circulation is crucial',
                'Early treatment is most effective'
            ],
            'rust': [
                'Keep foliage completely dry',
                'Good air flow prevents recurrence',
                'Check undersides of leaves daily'
            ],
            'blight': [
                'This is serious - act immediately',
                'Consider removing the entire plant',
                'Do not compost infected material'
            ],
            'yellowing': [
                'Check soil moisture first',
                'Could be overwatering or nutrient issue',
                'Remove yellow leaves to redirect energy'
            ],
            'wilting': [
                'Often reversible if caught early',
                'May indicate watering problems',
                'Keep plant well-hydrated but not soggy'
            ],
            'pest_damage': [
                'Isolation is critical to prevent spread',
                'Repeat treatments are necessary',
                'Check new plants before bringing home'
            ]
        }
        
        return tips_map.get(disease, ['Monitor closely', 'Be patient with treatment'])
    
    def _get_faq(self, disease: str) -> Dict:
        """Get FAQ for specific disease."""
        return {
            'how_long_treatment': 'Usually 2-4 weeks to see significant improvement',
            'will_plant_survive': 'With proper care, most plants recover unless severely affected',
            'can_spread': f'Yes, {disease} can spread to nearby plants - isolate if possible',
            'natural_remedy': 'Check "organic" treatment options in care plan',
            'safe_for_pets': 'Always check fungicide/pesticide labels for pet safety'
        }
    
    def _get_emergency_info(self, severity: str) -> Dict:
        """Get emergency information based on severity."""
        if severity == 'severe':
            return {
                'urgent': True,
                'recommendation': 'Consider consulting local extension office or expert',
                'resources': [
                    'Local agricultural extension office',
                    'Botanical gardens',
                    'Plant hospital services'
                ]
            }
        return {'urgent': False}
    
    def _get_default_care(self) -> Dict:
        """Get default care recommendations."""
        return {
            'immediate_actions': [
                'Assess plant condition carefully',
                'Ensure proper light and temperature',
                'Check soil moisture'
            ],
            'general_care': [
                'Monitor daily for changes',
                'Maintain consistent care schedule',
                'Keep plant clean'
            ]
        }

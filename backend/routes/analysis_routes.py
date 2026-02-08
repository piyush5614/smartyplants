"""Plant analysis routes - Main API endpoints."""

from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
from services import PlantAnalyzer, CareAdvisor
from services.gemini_analyzer import get_gemini_analyzer
from utils.validators import validate_file_upload, validate_image_file

analysis_bp = Blueprint('analysis', __name__, url_prefix='/api/v1')

# Initialize services
plant_analyzer = PlantAnalyzer()
care_advisor = CareAdvisor()


@analysis_bp.route('/analyze', methods=['POST'])
def analyze_plant():
    """
    Analyze plant image for disease detection.
    Uses Gemini AI for real disease detection when available,
    falls back to rule-based analysis otherwise.
    """
    try:
        # Validate request
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file provided'
            }), 400
        
        file = request.files['file']
        
        # Validate file
        validation = validate_file_upload(file)
        if not validation['valid']:
            return jsonify({
                'success': False,
                'error': validation['error']
            }), 400
        
        # Validate image
        image_validation = validate_image_file(file)
        if not image_validation['valid']:
            return jsonify({
                'success': False,
                'error': image_validation['error']
            }), 400
        
        # Read file bytes into memory so multiple readers can use it
        file.seek(0)
        from io import BytesIO
        file_bytes = file.read()
        file.seek(0)
        
        # Try Gemini AI analysis first (real disease detection)
        gemini = get_gemini_analyzer()
        current_app.logger.info(f"Gemini available: {gemini.is_available}, API key set: {bool(gemini.api_key)}")
        if gemini.is_available:
            image_io = BytesIO(file_bytes)
            ai_result, ai_message = gemini.analyze_image(image_io)
            current_app.logger.info(f"Gemini result: {ai_message}, got data: {ai_result is not None}")
            
            if ai_result:
                # Extract plant info
                plant_info = ai_result.get('plant_info', {})
                plant_name = plant_info.get('common_name', '') or ai_result.get('plant_type', 'Unknown')
                
                response = {
                    'success': True,
                    'analysis_type': 'ai',
                    'plant_info': plant_info,
                    'analysis': {
                        'success': True,
                        'plant_type': plant_name,
                        'is_healthy': ai_result.get('is_healthy', False),
                        'disease_detection': {
                            'primary_disease': ai_result.get('disease_name', 'Unknown'),
                            'disease_type': ai_result.get('disease_type', 'unknown'),
                            'confidence': ai_result.get('confidence', 50) / 100.0,
                            'severity': ai_result.get('severity', 'moderate'),
                            'description': ai_result.get('description', ''),
                            'common_causes': ai_result.get('causes', []),
                            'health_score': ai_result.get('health_score', 50),
                            'symptoms_observed': ai_result.get('symptoms_observed', []),
                            'risk_if_untreated': ai_result.get('risk_if_untreated', '')
                        },
                        'predictions': [{
                            'disease': ai_result.get('disease_name', 'Unknown'),
                            'confidence': ai_result.get('confidence', 50) / 100.0,
                            'severity': ai_result.get('severity', 'moderate'),
                            'description': ai_result.get('description', ''),
                            'common_causes': ai_result.get('causes', [])
                        }],
                        'timestamp': __import__('datetime').datetime.utcnow().isoformat() + 'Z'
                    },
                    'care_plan': {
                        'success': True,
                        'disease': ai_result.get('disease_name', 'Unknown'),
                        'severity': ai_result.get('severity', 'moderate'),
                        'confidence': ai_result.get('confidence', 50) / 100.0,
                        'immediate_actions': ai_result.get('immediate_actions', []),
                        'treatment': ai_result.get('treatment', {}),
                        'prevention': ai_result.get('prevention', []),
                        'watering_advice': ai_result.get('watering_advice', {}),
                        'recovery_timeline': ai_result.get('recovery_timeline', {}),
                        'risk_if_untreated': ai_result.get('risk_if_untreated', '')
                    }
                }
                return jsonify(response), 200
            else:
                # If rate limited, tell the user clearly
                if '429' in ai_message or 'Rate limit' in ai_message or 'quota' in ai_message.lower():
                    current_app.logger.warning(f"Gemini rate limited: {ai_message}")
                    return jsonify({
                        'success': False,
                        'error': 'AI analysis rate limit reached. Please wait 1-2 minutes and try again. (Free tier has limited requests per minute/day)'
                    }), 429
                current_app.logger.warning(f"Gemini analysis failed: {ai_message}, falling back to rule-based")
        
        # Fallback: rule-based analysis
        file.seek(0)
        confidence_threshold = request.args.get('confidence_threshold', 0.7, type=float)
        confidence_threshold = max(0.0, min(1.0, confidence_threshold))
        
        analysis_result = plant_analyzer.analyze_plant_image(file, confidence_threshold)
        
        if not analysis_result['success']:
            return jsonify(analysis_result), 400
        
        care_plan = care_advisor.generate_care_plan(analysis_result)
        
        response = {
            'success': True,
            'analysis_type': 'rule_based',
            'analysis': analysis_result,
            'care_plan': care_plan
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        current_app.logger.error(f"Analysis error: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500


@analysis_bp.route('/analyze/batch', methods=['POST'])
def analyze_batch():
    """
    Analyze multiple plant images.
    
    Request:
        - files: Multiple image files
    
    Response:
        - List of analysis results
    """
    try:
        if 'files' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No files provided'
            }), 400
        
        files = request.files.getlist('files')
        
        if not files or len(files) == 0:
            return jsonify({
                'success': False,
                'error': 'Empty file list'
            }), 400
        
        # Analyze each file
        results = []
        for file in files:
            # Validate
            validation = validate_file_upload(file)
            if not validation['valid']:
                results.append({
                    'success': False,
                    'filename': file.filename,
                    'error': validation['error']
                })
                continue
            
            file.seek(0)
            
            # Analyze
            analysis = plant_analyzer.analyze_plant_image(file)
            care = care_advisor.generate_care_plan(analysis) if analysis.get('success') else None
            
            results.append({
                'success': analysis.get('success', False),
                'filename': file.filename,
                'analysis': analysis,
                'care_plan': care
            })
        
        return jsonify({
            'success': True,
            'total_images': len(files),
            'successful': len([r for r in results if r['success']]),
            'results': results
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Batch analysis error: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500


@analysis_bp.route('/history/<session_id>', methods=['GET'])
def get_history(session_id):
    """
    Get analysis history for a session.
    
    Args:
        session_id: Unique session identifier
    
    Response:
        - List of previous analyses
    """
    try:
        # In production, retrieve from database
        # For now, return empty result
        return jsonify({
            'success': True,
            'session_id': session_id,
            'analyses': [],
            'total': 0
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"History retrieval error: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500


@analysis_bp.route('/diseases', methods=['GET'])
def get_disease_list():
    """Get list of detectable diseases."""
    from models import PlantDiseaseDetector
    
    detector = PlantDiseaseDetector()
    
    diseases = []
    for disease_name, info in detector.DISEASE_DATABASE.items():
        diseases.append({
            'name': disease_name,
            'severity': info.get('severity', 'unknown'),
            'description': info.get('description', ''),
            'common_causes': info.get('common_causes', [])
        })
    
    return jsonify({
        'success': True,
        'total_diseases': len(diseases),
        'diseases': diseases
    }), 200

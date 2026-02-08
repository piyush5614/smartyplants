"""Helper utilities and common functions."""

import uuid
from datetime import datetime
from typing import Any, Dict, List


def generate_session_id() -> str:
    """
    Generate unique session ID.
    
    Returns:
        Unique session identifier
    """
    return str(uuid.uuid4())


def generate_filename(original_filename: str, prefix: str = '') -> str:
    """
    Generate safe filename.
    
    Args:
        original_filename: Original filename
        prefix: Optional prefix for filename
        
    Returns:
        Safe filename
    """
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    unique_id = str(uuid.uuid4())[:8]
    
    # Extract extension
    if '.' in original_filename:
        ext = original_filename.rsplit('.', 1)[1].lower()
    else:
        ext = 'jpg'
    
    # Create safe filename
    if prefix:
        return f"{prefix}_{timestamp}_{unique_id}.{ext}"
    else:
        return f"{timestamp}_{unique_id}.{ext}"


def format_response(success: bool, data: Dict = None, error: str = None, 
                   message: str = None, status_code: int = 200) -> tuple:
    """
    Format API response.
    
    Args:
        success: Success status
        data: Response data
        error: Error message
        message: Custom message
        status_code: HTTP status code
        
    Returns:
        Tuple of (response_dict, status_code)
    """
    response = {
        'success': success,
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }
    
    if data:
        response['data'] = data
    
    if error:
        response['error'] = error
    
    if message:
        response['message'] = message
    
    return response, status_code


def truncate_string(text: str, max_length: int = 100) -> str:
    """
    Truncate string to max length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + '...'


def convert_to_dict(obj: Any) -> Dict:
    """
    Convert object to dictionary.
    
    Args:
        obj: Object to convert
        
    Returns:
        Dictionary representation
    """
    if hasattr(obj, 'to_dict'):
        return obj.to_dict()
    elif isinstance(obj, dict):
        return obj
    else:
        return obj.__dict__


def parse_confidence_scores(predictions: List[Dict]) -> List[Dict]:
    """
    Parse and format confidence scores.
    
    Args:
        predictions: List of predictions with scores
        
    Returns:
        Formatted predictions
    """
    formatted = []
    for pred in predictions:
        formatted_pred = {
            'disease': pred.get('disease', 'unknown'),
            'confidence': round(float(pred.get('confidence', 0)) * 100, 1),
            'confidence_level': _get_confidence_label(pred.get('confidence', 0)),
            'severity': pred.get('severity', 'unknown'),
            'description': pred.get('description', '')
        }
        formatted.append(formatted_pred)
    
    return formatted


def _get_confidence_label(confidence: float) -> str:
    """Get label for confidence score."""
    if confidence >= 0.9:
        return 'Very High'
    elif confidence >= 0.75:
        return 'High'
    elif confidence >= 0.6:
        return 'Moderate'
    elif confidence >= 0.4:
        return 'Fair'
    else:
        return 'Low'


def merge_dicts(base_dict: Dict, update_dict: Dict, deep: bool = False) -> Dict:
    """
    Merge two dictionaries.
    
    Args:
        base_dict: Base dictionary
        update_dict: Dictionary to merge
        deep: Deep merge (recursive)
        
    Returns:
        Merged dictionary
    """
    result = base_dict.copy()
    
    for key, value in update_dict.items():
        if deep and key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts(result[key], value, deep=True)
        else:
            result[key] = value
    
    return result


def calculate_percentage_change(old_value: float, new_value: float) -> float:
    """
    Calculate percentage change between values.
    
    Args:
        old_value: Original value
        new_value: New value
        
    Returns:
        Percentage change
    """
    if old_value == 0:
        return 0.0
    
    return ((new_value - old_value) / abs(old_value)) * 100

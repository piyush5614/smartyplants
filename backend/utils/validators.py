"""Input validation utilities."""

from werkzeug.datastructures import FileStorage
from PIL import Image
from io import BytesIO


def validate_file_upload(file: FileStorage) -> dict:
    """
    Validate uploaded file.
    
    Args:
        file: FileStorage object from Flask
        
    Returns:
        Dictionary with validation results
    """
    if not file or file.filename == '':
        return {'valid': False, 'error': 'No file selected'}
    
    # Check file extension
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    filename = file.filename.lower()
    
    if '.' not in filename:
        return {'valid': False, 'error': 'File has no extension'}
    
    extension = filename.rsplit('.', 1)[1]
    
    if extension not in allowed_extensions:
        return {
            'valid': False,
            'error': f'Invalid file type. Allowed: {", ".join(allowed_extensions)}'
        }
    
    # Check file size (5MB limit)
    file.seek(0, 2)  # Seek to end
    file_size = file.tell()
    file.seek(0)  # Reset
    
    max_size = 5 * 1024 * 1024  # 5MB
    if file_size > max_size:
        return {
            'valid': False,
            'error': f'File too large. Maximum: 5MB, Got: {file_size / 1024 / 1024:.2f}MB'
        }
    
    return {'valid': True}


def validate_image_file(file: FileStorage) -> dict:
    """
    Validate image file content.
    
    Args:
        file: FileStorage object from Flask
        
    Returns:
        Dictionary with validation results
    """
    try:
        # Reset file pointer
        file.seek(0)
        
        # Try to open as image
        img = Image.open(file.stream)
        
        # Check image dimensions
        width, height = img.size
        min_size = (100, 100)
        max_size = (4096, 4096)
        
        if width < min_size[0] or height < min_size[1]:
            return {
                'valid': False,
                'error': f'Image too small. Minimum: {min_size}, Got: ({width}, {height})'
            }
        
        if width > max_size[0] or height > max_size[1]:
            return {
                'valid': False,
                'error': f'Image too large. Maximum: {max_size}, Got: ({width}, {height})'
            }
        
        # Check image format
        if img.format not in ['JPEG', 'PNG', 'GIF', 'WEBP']:
            return {
                'valid': False,
                'error': f'Unsupported image format: {img.format}'
            }
        
        return {
            'valid': True,
            'format': img.format,
            'size': (width, height)
        }
        
    except Exception as e:
        return {
            'valid': False,
            'error': f'Invalid image file: {str(e)}'
        }


def validate_confidence_threshold(threshold: float) -> dict:
    """
    Validate confidence threshold value.
    
    Args:
        threshold: Confidence threshold (0.0-1.0)
        
    Returns:
        Dictionary with validation results
    """
    if not isinstance(threshold, (int, float)):
        return {'valid': False, 'error': 'Threshold must be a number'}
    
    if threshold < 0.0 or threshold > 1.0:
        return {'valid': False, 'error': 'Threshold must be between 0.0 and 1.0'}
    
    return {'valid': True, 'value': float(threshold)}


def validate_session_id(session_id: str) -> dict:
    """
    Validate session ID format.
    
    Args:
        session_id: Session identifier
        
    Returns:
        Dictionary with validation results
    """
    if not session_id or not isinstance(session_id, str):
        return {'valid': False, 'error': 'Invalid session ID'}
    
    if len(session_id) < 8 or len(session_id) > 100:
        return {'valid': False, 'error': 'Session ID length invalid'}
    
    # Check for valid characters
    import re
    if not re.match(r'^[a-zA-Z0-9_-]+$', session_id):
        return {'valid': False, 'error': 'Session ID contains invalid characters'}
    
    return {'valid': True, 'session_id': session_id}

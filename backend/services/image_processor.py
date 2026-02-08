"""
Image processing module for Smart Plant Health Assistant.
Handles image upload, validation, encoding, and preprocessing.
Pure processing logic - NO AI prompts or UI code included.
"""

import base64
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
from pathlib import Path
from typing import Tuple, Optional, Dict
import mimetypes


class ImageProcessor:
    """
    Service for processing plant leaf images.
    Handles validation, encoding, resizing, preprocessing, and enhancement.
    Focus: Image processing only - NO AI logic.
    """
    
    # Image constraints
    MIN_SIZE = (100, 100)
    MAX_SIZE = (4096, 4096)
    TARGET_SIZE = (224, 224)
    ALLOWED_FORMATS = ['JPEG', 'PNG', 'GIF', 'WEBP']
    SUPPORTED_MIMETYPES = {'image/jpeg', 'image/png', 'image/gif', 'image/webp'}
    MAX_FILE_SIZE_MB = 10
    MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
    
    def __init__(self):
        """Initialize image processor."""
        self.processed_images = {}
    
    def validate_image(self, image_file) -> dict:
        """
        Validate image file for quality and format.
        
        Args:
            image_file: File-like object or file path
            
        Returns:
            Dictionary with validation results
        """
        try:
            # Check file size first
            if hasattr(image_file, 'seek') and hasattr(image_file, 'tell'):
                image_file.seek(0, 2)  # Seek to end
                file_size = image_file.tell()
                image_file.seek(0)  # Reset
                
                if file_size > self.MAX_FILE_SIZE_BYTES:
                    return {
                        'valid': False,
                        'error': f"File size exceeds {self.MAX_FILE_SIZE_MB}MB limit"
                    }
            
            # Open image
            if isinstance(image_file, str):
                image = Image.open(image_file)
            else:
                image = Image.open(image_file.stream if hasattr(image_file, 'stream') else image_file)
            
            # Check MIME type if available
            if hasattr(image_file, 'content_type'):
                if image_file.content_type not in self.SUPPORTED_MIMETYPES:
                    return {
                        'valid': False,
                        'error': f"Unsupported MIME type: {image_file.content_type}"
                    }
            
            # Check format
            if image.format not in self.ALLOWED_FORMATS:
                return {
                    'valid': False,
                    'error': f"Invalid format. Allowed: {self.ALLOWED_FORMATS}"
                }
            
            # Check size
            width, height = image.size
            if width < self.MIN_SIZE[0] or height < self.MIN_SIZE[1]:
                return {
                    'valid': False,
                    'error': f"Image too small. Minimum: {self.MIN_SIZE}"
                }
            
            if width > self.MAX_SIZE[0] or height > self.MAX_SIZE[1]:
                return {
                    'valid': False,
                    'error': f"Image too large. Maximum: {self.MAX_SIZE}"
                }
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            return {
                'valid': True,
                'format': image.format,
                'size': (width, height),
                'mode': image.mode
            }
            
        except Exception as e:
            return {
                'valid': False,
                'error': f"Image validation failed: {str(e)}"
            }
    
    def validate_image_format(self, image_file) -> Tuple[bool, str]:
        """
        Validate image format and file type.
        Checks: MIME type, file size, image integrity, format.
        
        Args:
            image_file: File-like object (from upload)
            
        Returns:
            Tuple of (is_valid: bool, message: str)
        """
        try:
            # Check file size
            if hasattr(image_file, 'seek') and hasattr(image_file, 'tell'):
                image_file.seek(0, 2)
                file_size = image_file.tell()
                image_file.seek(0)
                
                if file_size == 0:
                    return False, "File is empty"
                
                if file_size > self.MAX_FILE_SIZE_BYTES:
                    return False, f"File exceeds {self.MAX_FILE_SIZE_MB}MB limit"
            
            # Check MIME type
            if hasattr(image_file, 'content_type'):
                if image_file.content_type not in self.SUPPORTED_MIMETYPES:
                    return False, f"Unsupported MIME type: {image_file.content_type}"
            
            # Try to open and verify image
            try:
                if hasattr(image_file, 'stream'):
                    img = Image.open(image_file.stream)
                else:
                    image_file.seek(0)
                    img = Image.open(image_file)
                
                img.verify()
                image_file.seek(0)
                
                # Re-open for format check (verify closes the file)
                if hasattr(image_file, 'stream'):
                    img = Image.open(image_file.stream)
                else:
                    image_file.seek(0)
                    img = Image.open(image_file)
                
                if img.format.upper() not in self.ALLOWED_FORMATS:
                    return False, f"Unsupported image format: {img.format}"
                
                image_file.seek(0)
                return True, "Image format valid"
                
            except Exception as e:
                return False, f"Invalid image file: {str(e)}"
            
        except Exception as e:
            return False, f"Format validation error: {str(e)}"
    
    def encode_to_base64(self, image_file) -> Tuple[Optional[str], str]:
        """
        Encode image file to base64 string.
        Validates before encoding.
        
        Args:
            image_file: File-like object (from upload)
            
        Returns:
            Tuple of (base64_string or None, message: str)
        """
        try:
            # Validate format first
            is_valid, validation_msg = self.validate_image_format(image_file)
            if not is_valid:
                return None, f"Validation failed: {validation_msg}"
            
            # Reset file pointer
            if hasattr(image_file, 'seek'):
                image_file.seek(0)
            
            # Read file content
            if hasattr(image_file, 'stream'):
                image_data = image_file.stream.read()
            elif hasattr(image_file, 'read'):
                image_data = image_file.read()
            else:
                with open(image_file, 'rb') as f:
                    image_data = f.read()
            
            # Encode to base64
            base64_string = base64.b64encode(image_data).decode('utf-8')
            
            return base64_string, "Image successfully encoded to base64"
            
        except Exception as e:
            return None, f"Encoding error: {str(e)}"
    
    def preprocess_image(self, image_file) -> tuple:
        """
        Preprocess image for analysis.
        
        Args:
            image_file: File-like object or file path
            
        Returns:
            Tuple of (processed_array, original_image)
        """
        try:
            # Open image
            if isinstance(image_file, str):
                image = Image.open(image_file)
            else:
                image = Image.open(image_file.stream)
            
            # Ensure RGB
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize to target size
            image_resized = image.resize(self.TARGET_SIZE, Image.Resampling.LANCZOS)
            
            # Convert to numpy array
            image_array = np.array(image_resized, dtype=np.float32)
            
            # Normalize pixel values (0-1)
            image_normalized = image_array / 255.0
            
            return image_normalized, image
            
        except Exception as e:
            raise Exception(f"Image preprocessing failed: {str(e)}")
    
    def enhance_image(self, image_array: np.ndarray) -> np.ndarray:
        """
        Enhance image for better disease detection.
        
        Args:
            image_array: numpy array of image
            
        Returns:
            Enhanced image array
        """
        try:
            # Convert to 0-255 range for OpenCV
            image_uint8 = (image_array * 255).astype(np.uint8)
            
            # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
            lab = cv2.cvtColor(image_uint8, cv2.COLOR_RGB2LAB)
            l, a, b = cv2.split(lab)
            
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
            l = clahe.apply(l)
            
            enhanced = cv2.merge([l, a, b])
            enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2RGB)
            
            # Normalize back to 0-1
            return enhanced.astype(np.float32) / 255.0
            
        except Exception as e:
            print(f"Enhancement failed, returning original: {str(e)}")
            return image_array
    
    def extract_roi(self, image_array: np.ndarray, focus_areas: int = 5) -> list:
        """
        Extract regions of interest (ROI) from image.
        
        Args:
            image_array: numpy array of image
            focus_areas: number of ROI areas to extract
            
        Returns:
            List of ROI arrays
        """
        try:
            height, width = image_array.shape[:2]
            rois = []
            
            # Define ROI grid
            roi_height = height // 3
            roi_width = width // 3
            
            positions = [
                (0, 0), (0, roi_width), (0, 2*roi_width),
                (roi_height, 0), (roi_height, roi_width),
                (roi_height, 2*roi_width),
                (2*roi_height, 0), (2*roi_height, roi_width),
                (2*roi_height, 2*roi_width)
            ]
            
            # Extract top N regions based on focus_areas
            for i, (y, x) in enumerate(positions[:focus_areas]):
                roi = image_array[y:y+roi_height, x:x+roi_width]
                rois.append({
                    'index': i,
                    'position': (y, x),
                    'size': roi.shape,
                    'data': roi
                })
            
            return rois
            
        except Exception as e:
            print(f"ROI extraction failed: {str(e)}")
            return []
    
    def save_processed_image(self, image_array: np.ndarray, filename: str, output_dir: str) -> str:
        """
        Save processed image to disk.
        
        Args:
            image_array: numpy array of image
            filename: name for output file
            output_dir: directory to save image
            
        Returns:
            Path to saved file
        """
        try:
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            # Convert to 0-255 if normalized
            if image_array.max() <= 1.0:
                image_uint8 = (image_array * 255).astype(np.uint8)
            else:
                image_uint8 = image_array.astype(np.uint8)
            
            # Save using PIL
            image = Image.fromarray(image_uint8)
            file_path = output_path / filename
            image.save(file_path)
            
            return str(file_path)
            
        except Exception as e:
            raise Exception(f"Failed to save image: {str(e)}")
    
    def validate_image_dimensions(self, image_file) -> Tuple[bool, str]:
        """
        Validate image dimensions are within acceptable range.
        
        Args:
            image_file: File-like object or file path
            
        Returns:
            Tuple of (is_valid: bool, message: str)
        """
        try:
            # Open image
            if isinstance(image_file, str):
                img = Image.open(image_file)
            else:
                if hasattr(image_file, 'stream'):
                    img = Image.open(image_file.stream)
                else:
                    image_file.seek(0)
                    img = Image.open(image_file)
            
            width, height = img.size
            
            # Check minimum dimensions
            if width < self.MIN_SIZE[0] or height < self.MIN_SIZE[1]:
                return False, f"Image too small. Min: {self.MIN_SIZE}, Got: ({width}, {height})"
            
            # Check maximum dimensions
            if width > self.MAX_SIZE[0] or height > self.MAX_SIZE[1]:
                return False, f"Image too large. Max: {self.MAX_SIZE}, Got: ({width}, {height})"
            
            if hasattr(image_file, 'seek'):
                image_file.seek(0)
            
            return True, f"Dimensions valid: ({width}, {height})"
            
        except Exception as e:
            return False, f"Dimension validation error: {str(e)}"
    
    def get_image_info(self, image_file) -> Dict:
        """
        Extract metadata and information from image.
        
        Args:
            image_file: File-like object or file path
            
        Returns:
            Dictionary with image metadata
        """
        try:
            # Open image
            if isinstance(image_file, str):
                img = Image.open(image_file)
            else:
                if hasattr(image_file, 'stream'):
                    img = Image.open(image_file.stream)
                else:
                    image_file.seek(0)
                    img = Image.open(image_file)
            
            width, height = img.size
            
            info = {
                'format': img.format,
                'mode': img.mode,
                'size': (width, height),
                'width': width,
                'height': height,
                'aspect_ratio': width / height if height > 0 else 0,
                'has_alpha': img.mode in ('RGBA', 'LA', 'PA'),
                'info': img.info if hasattr(img, 'info') else {}
            }
            
            if hasattr(image_file, 'seek'):
                image_file.seek(0)
            
            return info
            
        except Exception as e:
            return {'error': f"Failed to extract image info: {str(e)}"}
    
    def convert_to_rgb(self, image_file) -> Tuple[Optional[Image.Image], str]:
        """
        Convert image to RGB format.
        
        Args:
            image_file: File-like object or file path
            
        Returns:
            Tuple of (PIL Image in RGB or None, message: str)
        """
        try:
            # Open image
            if isinstance(image_file, str):
                img = Image.open(image_file)
            else:
                if hasattr(image_file, 'stream'):
                    img = Image.open(image_file.stream)
                else:
                    image_file.seek(0)
                    img = Image.open(image_file)
            
            # Convert if needed
            if img.mode == 'RGB':
                if hasattr(image_file, 'seek'):
                    image_file.seek(0)
                return img, "Already in RGB format"
            
            rgb_img = img.convert('RGB')
            
            if hasattr(image_file, 'seek'):
                image_file.seek(0)
            
            return rgb_img, f"Converted from {img.mode} to RGB"
            
        except Exception as e:
            return None, f"RGB conversion error: {str(e)}"
    
    def image_to_array(self, image_file) -> Tuple[Optional[np.ndarray], str]:
        """
        Convert image file to numpy array.
        
        Args:
            image_file: File-like object or file path
            
        Returns:
            Tuple of (numpy array or None, message: str)
        """
        try:
            # Open and convert to RGB
            if isinstance(image_file, str):
                img = Image.open(image_file)
            else:
                if hasattr(image_file, 'stream'):
                    img = Image.open(image_file.stream)
                else:
                    image_file.seek(0)
                    img = Image.open(image_file)
            
            # Ensure RGB
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Convert to array
            array = np.array(img, dtype=np.uint8)
            
            if hasattr(image_file, 'seek'):
                image_file.seek(0)
            
            return array, f"Converted to array with shape {array.shape}"
            
        except Exception as e:
            return None, f"Array conversion error: {str(e)}"

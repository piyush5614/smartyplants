"""
AI Analyzer module for Smart Plant Health Assistant.
Handles API communication with AI models for plant disease analysis.
Pure API logic - NO UI code, NO authentication, NO conditions.
"""

import os
import json
from typing import Dict, Optional, Tuple
from prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE


class AIAnalyzer:
    """
    Service for communicating with AI API for plant analysis.
    Responsibilities: Send requests, receive responses, return structured output.
    Focus: Pure API communication only - NO logic, NO UI.
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        """
        Initialize AI Analyzer.
        
        Args:
            api_key: OpenAI API key (uses OPENAI_API_KEY env var if not provided)
            model: Model to use (default: gpt-4)
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.model = model
        self.system_prompt = SYSTEM_PROMPT
        
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not found. Set OPENAI_API_KEY environment variable "
                "or pass api_key parameter."
            )
        
        # Initialize API client (lazy import to avoid hard dependency)
        try:
            import openai
            openai.api_key = self.api_key
            self.client = openai
        except ImportError:
            raise ImportError(
                "openai package not installed. Install with: pip install openai"
            )
    
    def analyze_plant_image(
        self,
        image_base64: str,
        image_format: str = "jpeg",
        image_width: Optional[int] = None,
        image_height: Optional[int] = None,
        capture_timestamp: Optional[str] = None
    ) -> Tuple[Optional[Dict], str]:
        """
        Send plant image to AI for analysis.
        
        Args:
            image_base64: Base64 encoded image string
            image_format: Image format (jpeg, png, gif, webp)
            image_width: Image width in pixels (optional)
            image_height: Image height in pixels (optional)
            capture_timestamp: When image was captured (optional)
        
        Returns:
            Tuple of (analysis_result: dict or None, message: str)
        """
        try:
            # Validate inputs
            if not image_base64:
                return None, "Image base64 string is empty"
            
            if not image_base64.strip():
                return None, "Invalid base64 string"
            
            # Create user prompt with image metadata
            user_message = USER_PROMPT_TEMPLATE.format(
                image_width=image_width or 'Unknown',
                image_height=image_height or 'Unknown',
                image_format=image_format.upper(),
                capture_timestamp=capture_timestamp or 'Not specified'
            )
            
            # Send to AI API
            response = self.client.ChatCompletion.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": self.system_prompt
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": user_message
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/{image_format};base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            # Extract response content
            if not response or not response.get('choices'):
                return None, "Empty response from AI API"
            
            analysis_text = response['choices'][0]['message']['content']
            
            # Parse response into structured format
            result = self._parse_ai_response(analysis_text)
            
            return result, "Analysis completed successfully"
            
        except self.client.error.AuthenticationError:
            return None, "Invalid OpenAI API key"
        except self.client.error.RateLimitError:
            return None, "Rate limit exceeded. Please try again later."
        except self.client.error.APIError as e:
            return None, f"OpenAI API error: {str(e)}"
        except ImportError:
            return None, "OpenAI library not properly configured"
        except Exception as e:
            return None, f"Analysis error: {str(e)}"
    
    def _parse_ai_response(self, response_text: str) -> Dict:
        """
        Parse AI response into structured format.
        
        Args:
            response_text: Raw text response from AI
        
        Returns:
            Structured dictionary with analysis data
        """
        try:
            # Try to parse as JSON first (if AI returns structured JSON)
            try:
                parsed = json.loads(response_text)
                if isinstance(parsed, dict):
                    return parsed
            except json.JSONDecodeError:
                pass
            
            # Fall back to text parsing
            result = {
                'raw_analysis': response_text,
                'diagnosis': self._extract_diagnosis(response_text),
                'confidence': self._extract_confidence(response_text),
                'health_score': self._extract_health_score(response_text),
                'recommendations': self._extract_recommendations(response_text),
                'severity': self._extract_severity(response_text)
            }
            
            return result
            
        except Exception as e:
            return {
                'raw_analysis': response_text,
                'parse_error': str(e)
            }
    
    def _extract_diagnosis(self, text: str) -> str:
        """Extract disease diagnosis from response text."""
        lines = text.split('\n')
        for line in lines:
            if 'disease' in line.lower() or 'diagnosis' in line.lower():
                return line.strip()
        
        # Return first non-empty line as fallback
        for line in lines:
            if line.strip():
                return line.strip()
        
        return "Unable to determine diagnosis"
    
    def _extract_confidence(self, text: str) -> float:
        """Extract confidence percentage from response text."""
        import re
        
        # Look for percentage patterns (e.g., "85%", "confidence: 0.85")
        patterns = [
            r'(\d+(?:\.\d+)?)\s*%',  # 85% format
            r'confidence[:\s]+(\d+(?:\.\d+)?)',  # confidence: 0.85
            r'(\d+(?:\.\d+)?)\s*(?:confidence|probability)'  # 0.85 confidence
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text.lower())
            if matches:
                try:
                    value = float(matches[0])
                    # Normalize to 0-100 range if needed
                    if value <= 1.0:
                        return value * 100
                    return min(value, 100.0)
                except (ValueError, IndexError):
                    continue
        
        return 0.0
    
    def _extract_health_score(self, text: str) -> float:
        """Extract plant health score (0-100) from response text."""
        import re
        
        patterns = [
            r'health\s*score[:\s]+(\d+)',
            r'score[:\s]+(\d+)',
            r'(\d+)/100'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text.lower())
            if matches:
                try:
                    return float(matches[0])
                except (ValueError, IndexError):
                    continue
        
        return 50.0  # Default neutral score
    
    def _extract_severity(self, text: str) -> str:
        """Extract disease severity (mild, moderate, severe) from response text."""
        text_lower = text.lower()
        
        if 'severe' in text_lower or 'critical' in text_lower:
            return 'severe'
        elif 'moderate' in text_lower or 'medium' in text_lower:
            return 'moderate'
        elif 'mild' in text_lower or 'light' in text_lower:
            return 'mild'
        else:
            return 'unknown'
    
    def _extract_recommendations(self, text: str) -> list:
        """Extract action recommendations from response text."""
        recommendations = []
        lines = text.split('\n')
        
        in_recommendations = False
        for line in lines:
            line = line.strip()
            
            # Start capturing recommendations section
            if 'recommend' in line.lower() or 'action' in line.lower():
                in_recommendations = True
                continue
            
            # Stop capturing at end markers
            if in_recommendations and line and (
                line.startswith('##') or
                'Risk' in line or
                'Next' in line
            ):
                break
            
            # Add bullet points and numbered items
            if in_recommendations and line:
                if line.startswith(('-', '•', '*')) or line[0].isdigit():
                    recommendations.append(line.lstrip('-•* 0123456789. '))
        
        # Return first 5 recommendations
        return recommendations[:5] if recommendations else []
    
    def validate_api_key(self) -> Tuple[bool, str]:
        """
        Validate OpenAI API key.
        
        Returns:
            Tuple of (is_valid: bool, message: str)
        """
        try:
            # Try a simple API call to verify key
            response = self.client.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "user",
                        "content": "Hello"
                    }
                ],
                max_tokens=10
            )
            
            if response and response.get('choices'):
                return True, "API key is valid"
            else:
                return False, "API key validation failed"
                
        except self.client.error.AuthenticationError:
            return False, "Invalid or expired API key"
        except self.client.error.RateLimitError:
            return False, "Rate limit exceeded"
        except Exception as e:
            return False, f"Validation error: {str(e)}"
    
    def get_model_info(self) -> Dict:
        """
        Get information about current AI model configuration.
        
        Returns:
            Dictionary with model details
        """
        return {
            'model': self.model,
            'system_prompt_length': len(self.system_prompt),
            'user_prompt_template_length': len(USER_PROMPT_TEMPLATE),
            'api_configured': bool(self.api_key)
        }


# Singleton instance for convenient access
_analyzer_instance = None


def get_analyzer(api_key: Optional[str] = None, model: str = "gpt-4") -> AIAnalyzer:
    """
    Get or create AI analyzer instance.
    
    Args:
        api_key: OpenAI API key (optional)
        model: Model to use (optional)
    
    Returns:
        AIAnalyzer instance
    """
    global _analyzer_instance
    
    if _analyzer_instance is None:
        _analyzer_instance = AIAnalyzer(api_key=api_key, model=model)
    
    return _analyzer_instance

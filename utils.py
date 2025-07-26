# utils/conversation_manager.py

from datetime import datetime
from typing import Dict, List, Optional
import json

class ConversationManager:
    """
    Manages conversation context and history
    """
    
    def __init__(self):
        self.context = {}
        self.message_history = []
    
    def add_message(self, message_type: str, content: str, agent: str = None, metadata: Dict = None):
        """Add a message to conversation history"""
        message = {
            'type': message_type,
            'content': content,
            'agent': agent,
            'timestamp': datetime.now().isoformat(),
            'metadata': metadata or {}
        }
        self.message_history.append(message)
        self._update_context(message)
    
    def _update_context(self, message: Dict):
        """Update conversation context based on new message"""
        if message['agent']:
            self.context['last_agent'] = message['agent']
        
        # Track topics discussed
        if 'topics' not in self.context:
            self.context['topics'] = []
        
        # Extract topics from content (simplified)
        content_lower = message['content'].lower()
        topics = ['eviction', 'rent', 'deposit', 'repair', 'lease', 'damage', 'mold', 'leak']
        for topic in topics:
            if topic in content_lower and topic not in self.context['topics']:
                self.context['topics'].append(topic)
    
    def get_context(self) -> Dict:
        """Get current conversation context"""
        return self.context.copy()
    
    def get_recent_messages(self, count: int = 5) -> List[Dict]:
        """Get recent messages from history"""
        return self.message_history[-count:]
    
    def clear_context(self):
        """Clear conversation context and history"""
        self.context = {}
        self.message_history = []


# utils/image_processor.py

import base64
import io
from PIL import Image
from typing import Optional, Tuple, Dict
import hashlib

class ImageProcessor:
    """
    Handles image processing and analysis preparation
    """
    
    def __init__(self):
        self.supported_formats = ['PNG', 'JPEG', 'JPG', 'GIF', 'BMP']
        self.max_file_size = 10 * 1024 * 1024  # 10MB
        self.max_dimensions = (2048, 2048)
    
    def validate_image(self, image_data: bytes, filename: str) -> Tuple[bool, str]:
        """
        Validate uploaded image
        
        Args:
            image_data: Raw image bytes
            filename: Original filename
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        
        # Check file size
        if len(image_data) > self.max_file_size:
            return False, f"File size too large. Maximum size is {self.max_file_size // 1024 // 1024}MB"
        
        try:
            # Try to open and validate image
            image = Image.open(io.BytesIO(image_data))
            
            # Check format
            if image.format not in self.supported_formats:
                return False, f"Unsupported format. Supported formats: {', '.join(self.supported_formats)}"
            
            # Check dimensions
            if image.size[0] > self.max_dimensions[0] or image.size[1] > self.max_dimensions[1]:
                return False, f"Image too large. Maximum dimensions: {self.max_dimensions[0]}x{self.max_dimensions[1]}"
            
            return True, "Valid image"
            
        except Exception as e:
            return False, f"Invalid image file: {str(e)}"
    
    def preprocess_image(self, image_data: bytes) -> Tuple[bytes, Dict]:
        """
        Preprocess image for analysis
        
        Args:
            image_data: Raw image bytes
            
        Returns:
            Tuple of (processed_image_data, metadata)
        """
        
        try:
            image = Image.open(io.BytesIO(image_data))
            
            # Get original metadata
            metadata = {
                'original_size': image.size,
                'format': image.format,
                'mode': image.mode,
                'file_size': len(image_data)
            }
            
            # Resize if too large
            if image.size[0] > 1024 or image.size[1] > 1024:
                image.thumbnail((1024, 1024), Image.Resampling.LANCZOS)
                metadata['resized'] = True
                metadata['new_size'] = image.size
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
                metadata['converted_to_rgb'] = True
            
            # Save processed image
            output_buffer = io.BytesIO()
            image.save(output_buffer, format='JPEG', quality=85, optimize=True)
            processed_data = output_buffer.getvalue()
            
            metadata['processed_size'] = len(processed_data)
            metadata['compression_ratio'] = len(processed_data) / len(image_data)
            
            return processed_data, metadata
            
        except Exception as e:
            raise ValueError(f"Failed to preprocess image: {str(e)}")
    
    def extract_image_features(self, image_data: bytes) -> Dict:
        """
        Extract basic features from image for analysis
        
        Args:
            image_data: Image bytes
            
        Returns:
            Dictionary of extracted features
        """
        
        try:
            image = Image.open(io.BytesIO(image_data))
            
            # Basic image statistics
            features = {
                'dimensions': image.size,
                'aspect_ratio': image.size[0] / image.size[1],
                'total_pixels': image.size[0] * image.size[1],
                'format': image.format,
                'mode': image.mode
            }
            
            # Color analysis for RGB images
            if image.mode == 'RGB':
                # Convert to analyze
                pixels = list(image.getdata())
                
                # Average color
                avg_r = sum(p[0] for p in pixels) / len(pixels)
                avg_g = sum(p[1] for p in pixels) / len(pixels)
                avg_b = sum(p[2] for p in pixels) / len(pixels)
                
                features['average_color'] = (int(avg_r), int(avg_g), int(avg_b))
                
                # Brightness estimate
                brightness = (avg_r * 0.299 + avg_g * 0.587 + avg_b * 0.114)
                features['brightness'] = brightness
                features['is_dark'] = brightness < 100
                features['is_bright'] = brightness > 180
            
            # Generate image hash for deduplication
            features['image_hash'] = hashlib.md5(image_data).hexdigest()
            
            return features
            
        except Exception as e:
            return {'error': f"Failed to extract features: {str(e)}"}
    
    def encode_image_for_api(self, image_data: bytes) -> str:
        """
        Encode image for API transmission
        
        Args:
            image_data: Image bytes
            
        Returns:
            Base64 encoded string
        """
        return base64.b64encode(image_data).decode('utf-8')
    
    def decode_image_from_api(self, encoded_data: str) -> bytes:
        """
        Decode image from API response
        
        Args:
            encoded_data: Base64 encoded string
            
        Returns:
            Image bytes
        """
        return base64.b64decode(encoded_data)
    
    def create_thumbnail(self, image_data: bytes, size: Tuple[int, int] = (200, 200)) -> bytes:
        """
        Create thumbnail of image
        
        Args:
            image_data: Original image bytes
            size: Thumbnail size (width, height)
            
        Returns:
            Thumbnail image bytes
        """
        
        try:
            image = Image.open(io.BytesIO(image_data))
            image.thumbnail(size, Image.Resampling.LANCZOS)
            
            # Save thumbnail
            output_buffer = io.BytesIO()
            image.save(output_buffer, format='JPEG', quality=90)
            return output_buffer.getvalue()
            
        except Exception as e:
            raise ValueError(f"Failed to create thumbnail: {str(e)}")


# utils/response_formatter.py

from typing import Dict, List, Optional
import re

class ResponseFormatter:
    """
    Formats agent responses for consistent presentation
    """
    
    def __init__(self):
        self.max_response_length = 2000
        self.bullet_point_symbol = "•"
        self.section_divider = "\n---\n"
    
    def format_agent_response(self, content: str, agent_type: str, confidence: float = None) -> str:
        """
        Format response with agent-specific styling
        
        Args:
            content: Raw response content
            agent_type: Type of agent (agent1, agent2, router)
            confidence: Confidence score
            
        Returns:
            Formatted response string
        """
        
        # Add agent header
        headers = {
            'agent1': '🔍 **Issue Detection Analysis**',
            'agent2': '⚖️ **Tenancy Legal Guidance**',
            'router': '🏠 **Real Estate Assistant**'
        }
        
        header = headers.get(agent_type, '🤖 **Assistant**')
        
        # Add confidence indicator if provided
        if confidence and confidence > 0:
            confidence_text = f" (Confidence: {confidence:.0%})"
            header += confidence_text
        
        # Format the content
        formatted_content = self._format_content_structure(content)
        
        # Combine header and content
        return f"{header}\n\n{formatted_content}"
    
    def _format_content_structure(self, content: str) -> str:
        """
        Apply consistent formatting to content structure
        """
        
        # Ensure consistent bullet points
        content = re.sub(r'^[\-\*]\s+', f'{self.bullet_point_symbol} ', content, flags=re.MULTILINE)
        
        # Format bold headers
        content = re.sub(r'\*\*(.*?)\*\*:', r'**\1:**', content)
        
        # Ensure proper spacing around sections
        content = re.sub(r'\n\n\n+', '\n\n', content)
        
        # Truncate if too long
        if len(content) > self.max_response_length:
            content = content[:self.max_response_length] + "\n\n...[Response truncated for length]"
        
        return content
    
    def format_error_response(self, error_message: str, agent_type: str = 'router') -> str:
        """
        Format error responses consistently
        """
        
        return f"❌ **Error - {agent_type.title()}**\n\n{error_message}\n\nPlease try rephrasing your question or contact support if the issue persists."
    
    def format_clarification_request(self, options: List[str]) -> str:
        """
        Format clarification requests with options
        """
        
        response_parts = [
            "🤔 **Need Clarification**\n",
            "I'd like to help you with the right specialist! Please choose:",
            ""
        ]
        
        for i, option in enumerate(options, 1):
            response_parts.append(f"{i}. {option}")
        
        response_parts.append("\nWhat would you like help with?")
        
        return "\n".join(response_parts)
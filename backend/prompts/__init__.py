"""
Prompts module for Smart Plant Health Assistant.
Contains all AI prompts separated from logic code.
- system_prompt.py: AI system role and behavior
- user_prompt.py: User instructions for image analysis
"""

from .system_prompt import SYSTEM_PROMPT
from .user_prompt import USER_PROMPT_TEMPLATE

__all__ = ['SYSTEM_PROMPT', 'USER_PROMPT_TEMPLATE']

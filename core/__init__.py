"""
Core Module

This module contains the foundational configuration and prompt engineering
required for the CUNY Grade Glossary Chatbot.
"""

from .config import MODEL_NAME, OPENAI_API_KEY
from .prompts import get_system_prompt

__all__ = ["MODEL_NAME", "OPENAI_API_KEY", "get_system_prompt"]
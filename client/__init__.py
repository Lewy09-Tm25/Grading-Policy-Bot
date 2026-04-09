"""
Client Module

This module handles the direct communication with the LLM provider (OpenAI).
It is responsible for sending the conversation history and streaming back the response.
"""

from .llm_client import stream_openai_response

__all__ = ["stream_openai_response"]
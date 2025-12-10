"""
Preview and Review System Module

A spaced repetition learning system for previewing knowledge points in the morning
and reviewing them in the afternoon/evening.
"""

__version__ = "1.0.0"
__author__ = "Knowledge Review System Team"

from .main import router

__all__ = ["router"]

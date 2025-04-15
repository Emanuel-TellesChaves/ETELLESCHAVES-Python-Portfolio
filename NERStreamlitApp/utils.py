# Monkey patch for typing.TypeVar issue
import sys
import typing
if not hasattr(typing.TypeVar, '__class_getitem__'):
    # Add the method to make TypeVar compatible with subscripting
    def _class_getitem(cls, key):
        return cls
    typing.TypeVar.__class_getitem__ = classmethod(_class_getitem)

import json
import os
import re
from typing import Dict, List, Tuple, Any, Optional

def load_sample_texts() -> Dict[str, str]:
    """
    Load sample texts from the sample_texts directory.
    
    Returns:
        Dict[str, str]: Dictionary with filename as key and text content as value
    """
    sample_texts = {}
    sample_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_texts")
    
    if os.path.exists(sample_dir):
        for filename in os.listdir(sample_dir):
            if filename.endswith(".txt"):
                file_path = os.path.join(sample_dir, filename)
                with open(file_path, "r", encoding="utf-8") as file:
                    sample_texts[filename] = file.read()
    
    return sample_texts

def validate_pattern(pattern: str) -> Tuple[bool, Optional[str], Any]:
    """
    Validate if a pattern string is correctly formatted.
    
    Args:
        pattern (str): The pattern string to validate
        
    Returns:
        Tuple[bool, Optional[str], Any]: 
            - Success status
            - Error message if any
            - Parsed pattern if valid
    """
    if not pattern.strip():
        return False, "Pattern cannot be empty", None
    
    # Check if it's a simple phrase pattern
    if not (pattern.startswith('[') and pattern.endswith(']')):
        # Simple string pattern
        return True, None, pattern.strip()
    
    # It should be a JSON pattern
    try:
        parsed_pattern = json.loads(pattern)
        # Verify it's a list of dictionaries
        if not isinstance(parsed_pattern, list):
            return False, "Pattern must be a list of dictionaries", None
        
        for item in parsed_pattern:
            if not isinstance(item, dict):
                return False, "Each item in pattern must be a dictionary", None
        
        return True, None, parsed_pattern
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {str(e)}", None

def get_color_for_label(label: str) -> str:
    """
    Generate a consistent color for a given entity label.
    
    Args:
        label (str): The entity label
        
    Returns:
        str: Hex color code
    """
    # Generate a deterministic but distributed color based on the label
    label_sum = sum(ord(c) for c in label)
    hue = (label_sum * 137.5) % 360
    
    # Convert HSV to RGB (simplified with saturation=60%, value=90%)
    h = hue / 60
    s = 0.6
    v = 0.9
    
    c = v * s
    x = c * (1 - abs(h % 2 - 1))
    m = v - c
    
    if 0 <= h < 1:
        r, g, b = c, x, 0
    elif 1 <= h < 2:
        r, g, b = x, c, 0
    elif 2 <= h < 3:
        r, g, b = 0, c, x
    elif 3 <= h < 4:
        r, g, b = 0, x, c
    elif 4 <= h < 5:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x
    
    r = int((r + m) * 255)
    g = int((g + m) * 255)
    b = int((b + m) * 255)
    
    return f"#{r:02x}{g:02x}{b:02x}"

def format_pattern_for_display(pattern: Any) -> str:
    """
    Format a pattern for display in the UI.
    
    Args:
        pattern (Any): Pattern to format (string or list of dicts)
        
    Returns:
        str: Formatted pattern
    """
    if isinstance(pattern, str):
        return f'"{pattern}"'
    elif isinstance(pattern, list):
        return json.dumps(pattern, indent=2)
    return str(pattern) 
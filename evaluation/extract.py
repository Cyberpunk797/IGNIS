"""
Extract C++ code from model response.
Handles various code block formats and edge cases.
"""

import re
from typing import Optional, Tuple


def extract_cpp_code(response: str) -> Tuple[Optional[str], str]:
    """
    Extract C++ code from model response.
    
    Returns:
        Tuple of (extracted_code, reasoning_text)
        - extracted_code: The C++ code if found, None otherwise
        - reasoning_text: Everything before the code block (if any)
    """
    code = None
    reasoning = response
    
    patterns = [
        r'```cpp\s*\n(.*?)\n```',
        r'```C\+\+\s*\n(.*?)\n```',
        r'```c\+\+\s*\n(.*?)\n```',
        r'```\s*\n(.*?)\n```',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, response, re.DOTALL)
        if match:
            code = match.group(1).strip()
            reasoning = response[:match.start()].strip()
            break
    
    if not code:
        code = extract_main_function(response)
        if code:
            reasoning = response.replace(code, "").strip()
    
    return code, reasoning


def extract_main_function(text: str) -> Optional[str]:
    """Extract main() function from text."""
    pattern = r'(int\s+main\s*\([^)]*\)\s*\{.*?\n\})'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1)
    
    lines = text.split('\n')
    in_code = False
    code_lines = []
    
    for line in lines:
        if re.match(r'^#include', line) or re.match(r'^\s*int\s+main', line):
            in_code = True
        
        if in_code:
            code_lines.append(line)
            
            if line.strip().startswith('}') and len(code_lines) > 5:
                break
    
    if code_lines:
        return '\n'.join(code_lines)
    
    return None


def has_code_block(response: str) -> bool:
    """Check if response contains any code block."""
    return '```' in response or extract_main_function(response) is not None


def clean_code(code: str) -> str:
    """Clean extracted code."""
    lines = code.split('\n')
    cleaned = []
    
    for line in lines:
        if line.strip() and not line.strip().startswith('```'):
            cleaned.append(line)
    
    result = '\n'.join(cleaned)
    
    result = re.sub(r'^\s*```\s*$', '', result, flags=re.MULTILINE)
    
    return result.strip()

"""
Compile C++ code using g++.
Handles compilation and returns results.
"""

import subprocess
import tempfile
import os
from pathlib import Path
from typing import Tuple, Optional
import config


def compile_code(code: str, output_path: Optional[Path] = None) -> Tuple[bool, str, Path]:
    """
    Compile C++ code with g++.
    
    Args:
        code: C++ source code
        output_path: Optional path for binary output
        
    Returns:
        Tuple of (success, error_message, binary_path)
        - success: True if compilation succeeded
        - error_message: Compilation error if any
        - binary_path: Path to compiled binary
    """
    if output_path is None:
        fd, output_path_str = tempfile.mkstemp(suffix='.exe', dir=config.TEMP_DIR)
        os.close(fd)
        output_path = Path(output_path_str)
    else:
        output_path = Path(output_path)
    
    src_fd, src_path = tempfile.mkstemp(suffix='.cpp', dir=config.TEMP_DIR)
    try:
        os.write(src_fd, code.encode('utf-8'))
        os.close(src_fd)
        
        cmd = [config.COMPILER] + config.COMPILE_FLAGS + [
            '-o', str(output_path),
            src_path
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            return True, "", output_path
        else:
            return False, result.stderr, output_path
            
    except subprocess.TimeoutExpired:
        return False, "Compilation timed out", output_path
    except Exception as e:
        return False, str(e), output_path
    finally:
        if os.path.exists(src_path):
            try:
                os.remove(src_path)
            except:
                pass


def check_compiler() -> Tuple[bool, str]:
    """
    Check if g++ is available.
    
    Returns:
        Tuple of (available, version_string)
    """
    try:
        result = subprocess.run(
            [config.COMPILER, '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version = result.stdout.split('\n')[0]
            return True, version
        return False, "g++ not found"
    except FileNotFoundError:
        return False, "g++ not installed"
    except Exception as e:
        return False, str(e)


def cleanup_temp_files():
    """Clean up temporary files."""
    import glob
    for pattern in ['*.exe', '*.cpp', '*.o']:
        for f in glob.glob(str(config.TEMP_DIR / pattern)):
            try:
                os.remove(f)
            except:
                pass

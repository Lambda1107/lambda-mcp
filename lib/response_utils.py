"""
Common utilities for handling tool responses.
"""
import json
import tempfile
import os
from tokenizers import Tokenizer

# Load tokenizer for accurate token counting
tokenizer = Tokenizer.from_pretrained("gpt2")

# Get max token limit from environment or use default
MAX_TOKEN_NUM = int(os.environ.get("LAMBDA_MCP_MAX_TOKEN_NUM", "30000"))


def handle_large_response(data, max_tokens: int = MAX_TOKEN_NUM) -> str:
    """
    Handle potentially large response data.
    If data exceeds token limit, save to file and return file info.
    
    Args:
        data: Data to return (will be JSON serialized)
        max_tokens: Maximum token count before saving to file
        
    Returns:
        JSON string of data or file info if too large
    """
    result_str = json.dumps(data, ensure_ascii=False, indent=2)
    token_count = len(tokenizer.encode(result_str))
    
    if token_count > max_tokens:
        # Write result to temporary file
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.json',
            delete=False,
            encoding='utf-8'
        ) as temp_file:
            temp_file.write(result_str)
            temp_file_path = temp_file.name
        
        return json.dumps({
            "type": "file",
            "path": temp_file_path,
            "reason": f"Result exceeds {max_tokens} tokens (got {token_count} tokens). Result saved to file.",
            "size_bytes": len(result_str.encode('utf-8'))
        })
    else:
        return result_str

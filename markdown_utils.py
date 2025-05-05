import re

def clean_markdown(text: str) -> str:
    """
    Clean and fix malformed Markdown text.
    
    Args:
        text: The Markdown text to clean
        
    Returns:
        str: Cleaned Markdown text
    """
    # Remove incomplete links
    text = re.sub(r'\[([^\[\]]*?)(?=\s*$|\n)', r'\1', text)
    # Remove links with invalid URLs
    text = re.sub(r'\[([^\[\]]*?)\]\s*(\([^)]*$)', r'\1', text)
    # Remove any remaining malformed markdown
    text = re.sub(r'\[([^\[\]]*?)\]\(\)', r'\1', text)
    return text

def sanitize_filename(name: str) -> str:
    """
    Sanitize a string to be used as a filename.
    
    Args:
        name: The string to sanitize
        
    Returns:
        str: Sanitized filename
    """
    import string
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    sanitized = ''.join(c for c in name if c in valid_chars)
    return sanitized.strip() 
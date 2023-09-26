import re


def urlencode(s):
    # urlencode <string>
    # Use Python's urllib.parse.quote to encode the string
    from urllib.parse import quote
    return quote(s, safe='')


def sanitize(filename):
    # Define a regex pattern to match characters not allowed in file names
    invalid_chars = r'[\/:*?"<>|]'
    # Replace invalid characters with underscores
    sanitized_filename = re.sub(invalid_chars, '_', filename)
    # Trim any leading or trailing spaces and dots
    sanitized_filename = sanitized_filename.strip('. ')
    # Ensure the filename is not empty
    if not sanitized_filename:
        sanitized_filename = 'unnamed_file'
    return sanitized_filename
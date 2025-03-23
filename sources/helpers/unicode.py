def unicode(char: str) -> str:
    code_point = ord(char)
    hex_code = f"U+{code_point:04X}"
    return hex_code

import re

def sanitize_text(text: str) -> str:
    text = text.strip()

    if len(text) > 2000:
        raise ValueError("Input too long")

    blacklist = [
        r"<script.*?>",
        r"</script>",
        r"DROP TABLE",
        r"--"
    ]

    for pattern in blacklist:
        if re.search(pattern, text, re.IGNORECASE):
            raise ValueError("Malicious input")

    return text

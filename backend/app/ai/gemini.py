import os, json, requests

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def analyze_feedback(text: str) -> dict:
    prompt = f"""
You are validating website feedback.

Return ONLY JSON:
- valid: boolean
- category: bug | feature | ux | performance | content | other

Feedback:
\"\"\"{text}\"\"\"
"""

    response = requests.post(
        "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent",
        params={"key": GEMINI_API_KEY},
        json={"contents": [{"parts": [{"text": prompt}]}]},
        timeout=5
    )

    output = response.json()["candidates"][0]["content"]["parts"][0]["text"]
    return json.loads(output)

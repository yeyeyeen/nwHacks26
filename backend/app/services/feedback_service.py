from app.security.sanitize import sanitize_text
from app.ai.gemini import analyze_feedback
from app.services.db import feedback_collection

def handle_feedback(input: dict):
    """
    input format:
    {
      "site_id": "abc123",
      "payload": {
        "message": "feedback text here"
      }
    }
    """

    site_id = input["site_id"]
    raw_text = input["payload"]["message"]

    # STEP 5A — sanitize (non-AI)
    clean_text = sanitize_text(raw_text)

    # STEP 5B — Gemini legitimacy check
    try:
        ai_result = analyze_feedback(clean_text)
    except Exception:
        ai_result = {"valid": True, "category": "other"}  # fail open

    if not ai_result["valid"]:
        return {
            "accepted": False,
            "reason": "Non-actionable feedback"
        }

    # STEP 6 — save to MongoDB
    doc = {
        "site_id": site_id,
        "text": clean_text,
        "category": ai_result["category"]
    }

    feedback_collection.insert_one(doc)

    return {
        "accepted": True,
        "category": ai_result["category"]
    }

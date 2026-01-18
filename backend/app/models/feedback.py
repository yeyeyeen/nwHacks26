from pydantic import BaseModel

class Feedback(BaseModel):
    user_id: str  # From Supabase
    repo_url: str  # GitHub repo URL
    name: str
    email: str
    message: str
    feedback_type: str = "bug"  # bug, feature, improvement, etc.

from pydantic import BaseModel

class Feedback(BaseModel):
    name: str
    email: str
    message: str

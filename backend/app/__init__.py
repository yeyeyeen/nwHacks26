from fastapi import FastAPI

# Create FastAPI app
app = FastAPI(
    title="Simple REST API",
    description="A basic REST controller with FastAPI",
    version="1.0.0"
)

# Import routers after app is created to avoid circular imports
from app.controller import main_controller, feedback

# Include all routers
app.include_router(main_controller.router)
app.include_router(feedback.router, prefix="/api", tags=["feedback"])


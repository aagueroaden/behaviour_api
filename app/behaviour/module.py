from app.behaviour.controller import behaviour_controller
from fastapi import APIRouter

behaviour_module = APIRouter()

# Register the behaviour controller (routes)
behaviour_module.include_router(behaviour_controller, prefix="/behaviour", tags=["Behaviour"])

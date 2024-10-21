from app.mvp_logging.controllers import mvp_log_controller
from fastapi import APIRouter

mvp_log_module = APIRouter()

mvp_log_module.include_router(mvp_log_controller, prefix="/mvp_log", tags=["MVP Log"])


from fastapi import APIRouter, Depends, status
from app.mvp_logging.services import MVPLogService
from app.mvp_logging.schemas import CreateMVPLog, MVPLog
from app.dependencies import get_mvp_log_service, validate_public_api_key

mvp_log_controller = APIRouter()


@mvp_log_controller.post(
    path="/log",
    response_model=MVPLog,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(validate_public_api_key)]
)
async def create_mvp_log(
    mvp_log: CreateMVPLog,
    mvp_log_service: MVPLogService = Depends(get_mvp_log_service),
) -> MVPLog:
    return mvp_log_service.create(mvp_log=mvp_log)

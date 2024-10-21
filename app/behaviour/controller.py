from app.dependencies import get_behaviour_service, validate_public_api_key
from app.behaviour.service import BehaviourService
from app.behaviour.schemas import (
    Action,
    Log,
    Site,
    CreateAction,
    CreateLog,
    CreateSite,
)
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from typing import List

behaviour_controller = APIRouter()


@behaviour_controller.post(
    path="/site",
    response_model=Site,
    description="Create a Site for later configuration",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(validate_public_api_key)]
)
async def create_site(
    site: CreateSite,
    service: BehaviourService = Depends(get_behaviour_service),
) -> Site:
    return service.create_site(site)


@behaviour_controller.get(path="/sites", dependencies=[Depends(validate_public_api_key)])
async def get_all_sites(
    service: BehaviourService = Depends(get_behaviour_service)
) -> List[Site]:
    return service.get_all_sites()


@behaviour_controller.post(
    path="/action",
    response_model=Action,
    status_code=status.HTTP_201_CREATED,
    description="Creates actions that would be captured for a site",
    dependencies=[Depends(validate_public_api_key)],
)
async def create_action(
    action: CreateAction,
    service: BehaviourService = Depends(get_behaviour_service)
) -> Action:
    return service.create_action(action=action)


@behaviour_controller.get(
    path="/{site_id}/actions",
    dependencies=[Depends(validate_public_api_key)]
)
async def get_site_actions(
    site_id: int,
    service: BehaviourService = Depends(get_behaviour_service)
) -> List[Action]:
    return service.get_actions_of_site(site_id=site_id)


@behaviour_controller.get(
    path="/actions",
    response_model=List[Action],
    dependencies=[Depends(validate_public_api_key)],
)
async def get_all_actions(
    service: BehaviourService = Depends(get_behaviour_service)
) -> List[Action]:
    return service.get_all_actions()


@behaviour_controller.post(
    path="/log",
    response_model=Log,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(validate_public_api_key)],
)
async def create_log(
    log: CreateLog,
    service: BehaviourService = Depends(get_behaviour_service)
) -> Log:
    return service.create_log(log)


@behaviour_controller.get(
    path="/log/{log_id}",
    description="Obtains a log by Id",
    response_model=Log,
    dependencies=[Depends(validate_public_api_key)],
)
async def get_log(
    log_id: int,
    service: BehaviourService = Depends(get_behaviour_service)
) -> Log:
    log = service.get_log(log_id)
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Log {log_id} not found"
        )
    return log

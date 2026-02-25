from typing import Tuple

from fastapi import APIRouter, FastAPI


def include_routers(app: FastAPI, routers: Tuple[APIRouter]) -> None:
    for router in routers:
        app.include_router(router)

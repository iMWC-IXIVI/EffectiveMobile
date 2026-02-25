from fastapi import FastAPI

from api.v1 import test_router, user_router
from utils import include_routers


ROUTERS_LIST = (test_router, user_router, )


app = FastAPI(title='EffectiveMobile Task', version='0.0.1')

include_routers(app, ROUTERS_LIST)

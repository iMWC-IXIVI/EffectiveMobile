from fastapi import FastAPI

from api.v1 import test_router


app = FastAPI(title='EffectiveMobile Task', version='0.0.1')

app.include_router(router=test_router)

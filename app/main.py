from fastapi import FastAPI, Depends

from app.dependencies import Base, engine, get_db
from app.models import user_model, task_model
from app.routers.users_router import router

app = FastAPI(dependencies=[Depends(get_db)])

app.include_router(router)
Base.metadata.create_all(bind=engine)

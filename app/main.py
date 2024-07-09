from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.dependencies import Base, engine, get_db
from app.models import user_model, task_model
from app.routers import users_router, tasks_router

app = FastAPI(dependencies=[Depends(get_db)])

origins = [
    "http://localhost:3000",  # Your Next.js frontend URL
    "http://localhost:8000",  # Your FastAPI backend URL (optional, usually not needed)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(users_router.router)
app.include_router(tasks_router.router)
Base.metadata.create_all(bind=engine)

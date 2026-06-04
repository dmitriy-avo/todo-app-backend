from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from app.api.routers.category import category_router
from app.core.config import settings
from app.db.session import engine
from app.models.base import Base
from app.api.routers.task import task_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print('starting lifespan')
    Base.metadata.create_all(engine)
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(task_router)
app.include_router(category_router)

app.add_middleware(CORSMiddleware,
                   allow_origins=settings.cors_allowed_origins,
                   allow_methods=["*"],
                   )






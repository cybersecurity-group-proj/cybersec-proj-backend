from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes.routes import api_router
import asyncio
from fastapi.middleware.cors import CORSMiddleware
from app.config import Config

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("API is up")
    yield
    print("API is down")


version = "v1"

app = FastAPI(
    title="cybersec-proj API",
    version=version,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.FRNT_END_URL,
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"]
)



app.include_router(api_router, prefix=f"/api/{version}")
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.cats.router import router as cats_router
from src.missions.router import router as missions_targets_router

app = FastAPI()

app.include_router(cats_router)
app.include_router(missions_targets_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi import FastAPI
from routes.games import game_router
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from models.game import Game
from sqlmodel import SQLModel

app = FastAPI()

SQLModel.metadata.create_all(engine)

app.include_router(game_router)
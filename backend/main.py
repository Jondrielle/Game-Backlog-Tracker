from fastapi import FastAPI
from routes.games import game_router

app = FastAPI()

app.include_router(game_router)
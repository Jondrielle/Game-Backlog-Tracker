from fastapi import APIRouter
from utils.igdb_utils import search_games


router = APIRouter()

@router.get("/games/search")
async def search_game_database(name: str):
	return await search_games(name)
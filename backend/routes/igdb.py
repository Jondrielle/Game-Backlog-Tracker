from fastapi import APIRouter, Depends, Query, HTTPException
from httpx import HTTPError

from utils.igdb_utils import search_games
from routes.auth import get_current_user
from models.user import User

igdb_router = APIRouter(prefix="/games", tags=["IGDB"])

router = APIRouter()

@router.get("/search")
async def search_game_database(
	q: str = Query(min_length=1, max_length=100),
    current_user: User = Depends(get_current_user),
):
    try:
        return await search_games(q)
    except HTTPError:
        raise HTTPException(
            status_code=502,
            detail="Unable to search IGDB right now",
        )

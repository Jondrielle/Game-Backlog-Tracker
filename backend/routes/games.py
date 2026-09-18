from fastapi import APIRouter,Depends,HTTPException
from schemas.game import GameBase,CreateGame,GameRead,UpdateGame
from enums.enum import Platform, Status, Genre
from sqlmodel import Session,select
from database import get_session
from models.game import Game
from typing import List,Optional

game_router = APIRouter()

# Retrieve all games filtered and unfiltered
@game_router.get("/", response_model=List[GameRead])
async def get_games(name: Optional[str] = None,status: Optional[Status]=None,genre: Optional[Genre]=None,
					platform: Optional[Platform]=None, session: Session = Depends(get_session),
					skip: int=0, limit:int=10):
	statement = select(Game)

	# Filters
	if name is not None:
		statement = statement.where(Game.name.ilike(f"%{name}%"))
	if status is not None:
	    statement = statement.where(Game.status == status)
	if genre is not None:
	    statement = statement.where(Game.genre == genre)
	if platform is not None:
	    statement = statement.where(Game.platform == platform)
	
	# Pagnation
	statement = statement.offset(skip).limit(limit)

	games = session.exec(statement).all()
	return games

# Retrieve a single game
@game_router.get("/game/{game_id}", response_model=GameRead)
async def get_game(game_id:int,session: Session = Depends(get_session)):
	statement = select(Game).where(Game.id == game_id)
	game = session.exec(statement).first()

	if game is None:
		raise HTTPException(status_code=404,detail="Game not found")
		
	return game

# Create a single game
@game_router.post("/",response_model = GameRead)
async def create_game(game:CreateGame,session: Session = Depends(get_session)):

	new_game = Game(
		name = game.name,
		status = game.status,
		rating = game.rating,
		notes = game.notes,
		platform = game.platform,
		genre = game.genre,
		release_date = game.release_date,
		date_completed = game.date_completed
	)

	session.add(new_game)
	session.commit()
	session.refresh(new_game)

	return new_game

# Delete a single game
@game_router.delete("/game/{game_id}")
async def delete_game(game_id: int, session: Session = Depends(get_session)):
	statement = select(Game).where(Game.id == game_id)
	game = session.exec(statement).first()
	
	if game is None:
		raise HTTPException(status_code=404,detail="Game not found")

	session.delete(game)
	session.commit()
	return {"message": "Game Deleted Successfully"}

# Clear games
@game_router.delete("/game")
async def clear(session: Session = Depends(get_session)):
	statement = select(Game)
	games = session.exec(statement).all()

	for game in games:
		session.delete(game)
	
	session.commit()

	return {"message": "List Cleared"}

# Update a game
@game_router.patch("/game/{game_id}", response_model = GameRead)
async def update_game(game_id: int, updated_game: UpdateGame, session: Session = Depends(get_session)):
	statement = select(Game).where(Game.id == game_id)
	game = session.exec(statement).first()

	if game is None:
		raise HTTPException(status_code=404,detail="Game not found")

	if updated_game.name is not None:
		game.name = updated_game.name

	if updated_game.status is not None:
		game.status = updated_game.status

	if updated_game.rating is not None:
		game.rating = updated_game.rating

	if updated_game.notes is not None:
		game.notes = updated_game.notes

	if updated_game.platform is not None:
		game.platform = updated_game.platform 

	if updated_game.genre is not None:
		game.genre = updated_game.genre

	if updated_game.release_date is not None:
		game.release_date = updated_game.release_date

	if updated_game.date_completed is not None:
		game.date_completed = updated_game.date_completed

	session.commit()
	session.refresh(game)

	return game

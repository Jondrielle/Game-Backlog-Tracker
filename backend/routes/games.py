from fastapi import APIRouter
from schemas.game import GameBase,CreateGame,Game

game_router = APIRouter()

counter_id = 0

@game_router.get("/")
async def get_game():
	return "Starting fastapi route connection"

@game_router.post("/",response_model = Game)
async def create_game(game:CreateGame):
	global counter_id 

	new_game = Game(
		id = counter_id,
		name = game.name,
		status = game.status,
		rating = game.rating,
		notes = game.notes,
		platform = game.platform,
		genre = game.genre,
		release_date = game.release_date,
		date_completed = game.date_completed
	)

	counter_id += 1

	return new_game


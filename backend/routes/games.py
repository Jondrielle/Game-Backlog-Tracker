from fastapi import APIRouter
from schemas.game import GameBase,CreateGame,Game,UpdateGame
from enums.enum import Platform, Status, Genre

game_router = APIRouter()

counter_id = 0

games = []

@game_router.get("/")
async def get_game():
	return games

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
	games.append(new_game)

	return new_game

@game_router.delete("/game/{game_id}")
async def delete_game(game_id: int):
	for game in games:
		if game.id == game_id:
			games.remove(game)
			return {"message": "Game Deleted Successfully"}

@game_router.patch("/game/{game_id}", response_model = Game)
async def update_game(game_id: int, updated_game: UpdateGame):
	for game in games:
		if game.id == game_id:
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

			return game

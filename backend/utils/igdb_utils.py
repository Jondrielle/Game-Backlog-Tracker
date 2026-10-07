import os
import httpx
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()


def get_client_id():
	return os.getenv("IGDB_CLIENT_ID")


def get_client_secret():
	return os.getenv("IGDB_CLIENT_SECRET")


async def get_access_token():
	client_id = get_client_id()
	client_secret = get_client_secret()

	async with httpx.AsyncClient() as client:
		response = await client.post(
			"https://id.twitch.tv/oauth2/token",
			params={
				"client_id": client_id,
				"client_secret": client_secret,
				"grant_type": "client_credentials"
			}
		)

	response.raise_for_status()

	data = response.json()

	return data["access_token"]


async def search_games(name):
	access_token = await get_access_token()

	async with httpx.AsyncClient() as client:
		response = await client.post(
		"https://api.igdb.com/v4/games",
		headers={
			"Client-ID": get_client_id(),
			"Authorization": f"Bearer {access_token}"
		},
		content=f'''
			search "{name}";
			fields name, platforms.name, genres.name, first_release_date;
			limit 10;
		'''
		)

		response.raise_for_status()
		games = response.json()

	return [
		format_game(game)
		for game in games
	]



def format_game(game):
	release_date = None

	if "first_release_date" in game:
		release_date = datetime.fromtimestamp(
            game["first_release_date"]
        ).strftime("%Y-%m-%d")

        
	return {
        "id": game["id"],
        "name": game["name"],
        "genres": [
            genre["name"]
            for genre in game.get("genres", [])
        ],
        "platforms": [
            platform["name"]
            for platform in game.get("platforms", [])
        ],
        "release_date": release_date
    }


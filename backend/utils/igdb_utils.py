
import os
import httpx
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv()

TWITCH_TOKEN_URL = "https://id.twitch.tv/oauth2/token"
IGDB_GAMES_URL = "https://api.igdb.com/v4/games"


def get_client_id():
    return os.getenv("IGDB_CLIENT_ID")


def get_client_secret():
    return os.getenv("IGDB_CLIENT_SECRET")


async def get_access_token():
    client_id = get_client_id()
    client_secret = get_client_secret()

    if not client_id or not client_secret:
        raise RuntimeError("IGDB credentials are not configured")

    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.post(
            TWITCH_TOKEN_URL,
            params={
                "client_id": client_id,
                "client_secret": client_secret,
                "grant_type": "client_credentials",
            },
        )
        response.raise_for_status()

    return response.json()["access_token"]


async def search_games(name: str):
    name = name.strip()

    if not name:
        return []

    access_token = await get_access_token()

    # Escape characters that could interfere with the IGDB query.
    safe_name = name.replace("\\", "\\\\").replace('"', '\\"')

    query = f'''
        search "{safe_name}";
        fields id, name, cover.image_id,platforms.name, genres.name, first_release_date;
        limit 10;
    '''

    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.post(
            IGDB_GAMES_URL,
            headers={
                "Client-ID": get_client_id(),
                "Authorization": f"Bearer {access_token}",
            },
            content=query,
        )
        response.raise_for_status()

    games = [format_game(game) for game in response.json()]

    for game in games:
        print(game["name"], "->", game["cover_url"])

    return games
    return [format_game(game) for game in response.json()]


def format_game(game):
    timestamp = game.get("first_release_date")

    release_date = (
        datetime.fromtimestamp(timestamp, tz=timezone.utc)
        .strftime("%Y-%m-%d")
        if timestamp is not None
        else None
    )

    cover = game.get("cover")
    image_id = cover.get("image_id") if cover else None

    # Build the URL only if IGDB provides an image ID.
    cover_url = (
        f"https://images.igdb.com/igdb/image/upload/t_cover_big/{image_id}.jpg"
        if image_id
        else None
    )

    return {
        "igdb_id": game["id"],
        "name": game["name"],
        "cover_url": cover_url,
        "genres": [
            genre["name"] for genre in game.get("genres", [])
        ],
        "platforms": [
            platform["name"] for platform in game.get("platforms", [])
        ],
        "release_date": release_date,
    }

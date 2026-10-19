from fastapi import APIRouter, Depends, HTTPException
from schemas.game import CreateGame, GameRead, UpdateGame
from enums.enum import Platform, Status, Genre as GenreEnum
from sqlmodel import Session, select
from sqlalchemy import func
from database import get_session
from models.game import Game, Genre, GenreGame
from models.user import User
from typing import Optional
from routes.auth import get_current_user



game_router = APIRouter()

def game_to_response(game: Game):
    return {
        "id": game.id,
        "name": game.name,
        "cover_url":game.cover_url,
        "status": game.status,
        "rating": game.rating,
        "notes": game.notes,
        "platform": game.platform,
        "genres": [genre.name for genre in game.genres],
        "release_date": game.release_date,
        "date_completed": game.date_completed
    }

# Retrieve all games, filtered and unfiltered
@game_router.get("/")
async def get_games(
    name: Optional[str] = None,
    status: Optional[Status] = None,
    genre: Optional[GenreEnum] = None,
    platform: Optional[Platform] = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 10
):

    # Build the main game query
    statement = select(Game).where(
        Game.user_id == current_user.id)

    if name is not None:
        statement = statement.where(
            Game.name.ilike(f"%{name}%")
        )

    if status is not None:
        statement = statement.where(
            Game.status == status
        )

    if genre is not None:
        statement = statement.join(
            GenreGame,
            Game.id == GenreGame.game_id
        ).join(
            Genre,
            Genre.id == GenreGame.genre_id
        ).where(
            Genre.name == genre.value
        )

    if platform is not None:
        statement = statement.where(
            Game.platform == platform
        )

    # Count matching games
    count_statement = select(
        func.count(func.distinct(Game.id))
    ).select_from(Game).where(
        Game.user_id == current_user.id)

    if name is not None:
        count_statement = count_statement.where(
            Game.name.ilike(f"%{name}%")
        )

    if status is not None:
        count_statement = count_statement.where(
            Game.status == status
        )

    if genre is not None:
        count_statement = count_statement.join(
            GenreGame,
            Game.id == GenreGame.game_id
        ).join(
            Genre,
            Genre.id == GenreGame.genre_id
        ).where(
            Genre.name == genre.value
        )

    if platform is not None:
        count_statement = count_statement.where(
            Game.platform == platform
        )

    total = session.exec(count_statement).one()

    # Pagination
    statement = statement.offset(skip).limit(limit)

    games = session.exec(statement).all()

    return {
        "games": games,
        "total": total
    }


# Retrieve a single game
@game_router.get("/game/{game_id}", response_model=GameRead)
async def get_game(
    game_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):

    statement = select(Game).where(
        Game.id == game_id,
        Game.user_id == current_user.id)

    game = session.exec(statement).first()

    if game is None:
        raise HTTPException(
            status_code=404,
            detail="Game not found"
        )

    return game


# Create a single game
@game_router.post("/", response_model=GameRead)
async def create_game(
    game: CreateGame,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):

    new_game = Game(
        user_id=current_user.id,
        name=game.name,
        cover_url=game.cover_url,
        status=game.status,
        rating=game.rating,
        notes=game.notes,
        platform=game.platform,
        release_date=game.release_date,
        date_completed=game.date_completed
    )

    session.add(new_game)
    session.commit()
    session.refresh(new_game)

    # Add genres
    for genre_name in game.genres:

        genre = session.exec(
            select(Genre).where(
                Genre.name == genre_name.value
            )
        ).first()

        # Create genre if it doesn't exist
        if genre is None:
            genre = Genre(
                name=genre_name.value
            )

            session.add(genre)
            session.commit()
            session.refresh(genre)

        # Connect game to genre
        link = GenreGame(
            game_id=new_game.id,
            genre_id=genre.id
        )

        session.add(link)

    session.commit()
    session.refresh(new_game)
    
    return game_to_response(new_game)
  


# Delete a single game

@game_router.delete("/game/{game_id}")
async def delete_game(
    game_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    game = session.exec(
        select(Game).where(
            Game.id == game_id,
            Game.user_id == current_user.id,
        )
    ).first()

    if game is None:
        raise HTTPException(
            status_code=404,
            detail="Game not found",
        )

    session.delete(game)
    session.commit()

    return {"message": "Game deleted successfully"}


# Clear all games
@game_router.delete("/game")
async def clear(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):

    statement = select(Game)

    games = session.exec(
        select(Game).where(
            Game.user_id == current_user.id,
        )
    ).all()

    if games is None:
        raise HTTPException(
            status_code=404,
            detail="Games not found",
        )

    for game in games:
        session.delete(game)

    session.commit()

    return {
        "message": "List Cleared"
    }


# Update a game
@game_router.patch("/game/{game_id}",response_model=GameRead)
async def update_game(
    game_id: int,
    updated_game: UpdateGame,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):

    statement = select(Game).where(
        Game.id == game_id,
        Game.user_id == current_user.id
    )

    game = session.exec(statement).first()

    if game is None:
        raise HTTPException(
            status_code=404,
            detail="Game not found"
        )

    # Update normal fields
    if updated_game.name is not None:
        game.name = updated_game.name

    if updated_game.cover_url is not None:
        game.cover_url = updated_game.cover_url

    if updated_game.status is not None:
        game.status = updated_game.status

    if updated_game.rating is not None:
        game.rating = updated_game.rating

    if updated_game.notes is not None:
        game.notes = updated_game.notes

    if updated_game.platform is not None:
        game.platform = updated_game.platform

    if updated_game.release_date is not None:
        game.release_date = updated_game.release_date

    if updated_game.date_completed is not None:
        game.date_completed = updated_game.date_completed

    # Update genres
    if updated_game.genres is not None:

        # Remove existing genre connections
        existing_links = session.exec(
            select(GenreGame).where(
                GenreGame.game_id == game.id
            )
        ).all()

        for link in existing_links:
            session.delete(link)

        session.commit()

        # Add new genre connections
        for genre_name in updated_game.genres:

            genre = session.exec(
                select(Genre).where(
                    Genre.name == genre_name.value
                )
            ).first()

            if genre is None:
                genre = Genre(
                    name=genre_name.value
                )

                session.add(genre)
                session.commit()
                session.refresh(genre)

            link = GenreGame(
                game_id=game.id,
                genre_id=genre.id
            )

            session.add(link)

    session.commit()
    session.refresh(game)

    return game
from datetime import date
from typing import Optional,List

from sqlmodel import SQLModel,Field, Relationship
from enums.enum import Status, Platform

class GenreGame(SQLModel, table=True):
	game_id: int = Field(foreign_key="game.id",primary_key=True)
	genre_id: int = Field(foreign_key="genre.id",primary_key=True)

class Game(SQLModel,table=True):
	id: Optional[int] = Field(default=None, primary_key=True)
	user_id: int = Field(foreign_key="user.id")
	name: str
	cover_url: Optional[str] = Field(default=None)
	status: Status
	rating: Optional[int] = Field(default=None,ge=1,le=5)
	notes:Optional[str] = Field(default=None, max_length = 500)
	platform: Platform
	genres: List["Genre"] = Relationship(
    back_populates="games",
    link_model=GenreGame)
	release_date: date
	date_completed: Optional[date] = None

class Genre(SQLModel, table=True):
	id: Optional[int] = Field(default=None, primary_key=True)
	name: str
	games: List["Game"] = Relationship(
    back_populates="genres",
    link_model=GenreGame)

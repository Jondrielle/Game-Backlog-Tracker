from datetime import date
from typing import Optional

from sqlmodel import SQLModel,Field 
from enums.enum import Status, Platform, Genre

class Game(SQLModel,table=True):
	id: Optional[int] = Field(default=None, primary_key=True)
	name: str
	status: Status
	rating: Optional[int] = Field(default=None,ge=1,le=5)
	notes:Optional[str] = Field(default=None, max_length = 500)
	platform: Platform
	release_date: date
	date_completed: Optional[date] = None

class Genre(SQLModel, table=True):
	id: Optional[int] = Field(default=None, primary_key=True)
	name: str

class Genre_Game(SQLModel, table=True):
	game_id: int = Field(foreign_key="game.id",primary_key=True)
	genre_id: int = Field(foreign_key="genre.id",primary_key=True)

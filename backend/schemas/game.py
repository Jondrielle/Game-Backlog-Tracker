from pydantic import BaseModel,Field
from datetime import date 
from typing import Optional
from enum import Platform,Status,Genre

class GameBase(BaseModel):
	name: str
	status: Status
	rating: int | None = Field(default= None,ge=1,le=5)
	notes:str | None = Field(default=None, max_length = 500)
	platform: Platform
	genre: Genre
	release_date: date
	date_completed: date | None = None

class Game(gameBase):
	id: int

class CreateGame(gameBase):
	pass



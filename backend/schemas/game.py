from pydantic import BaseModel,Field
from date import Date 
from enum import Platform,Status,Genre

class GameBase(BaseModel):
	name: str
	status: Status
	rating: int
	notes:str = Field(max_length = 500)
	platform: Platform
	genre: Genre
	release_year: Date
	date_completed: Date

class Game(gameBase):
	id: int

class CreateGame(gameBase):
	pass



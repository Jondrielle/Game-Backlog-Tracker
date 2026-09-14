from pydantic import BaseModel,Field
from datetime import date 
from typing import Optional
from enums.enum import Platform,Status,Genre

class GameBase(BaseModel):
	name: str
	status: Status
	rating: Optional[int] = Field(default= None,ge=1,le=5)
	notes:Optional[str] = Field(default=None, max_length = 500)
	platform: Platform
	genre: Genre
	release_date: date
	date_completed: Optional[date] = None

class Game(GameBase):
	id: int

class CreateGame(GameBase):
	pass

class UpdateGame(BaseModel):
	name: Optional[str] = None
	status: Optional[Status] = None
	rating: Optional[int] = Field(default= None,ge=1,le=5)
	notes:Optional[str] = Field(default=None, max_length = 500)
	platform: Optional[Platform] = None
	genre: Optional[Genre] = None
	release_date: Optional[date] = None
	date_completed: Optional[date] = None



from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List
from enums.enum import Platform, Status, Genre as GenreEnum


class GameBase(BaseModel):
    name: str
    cover_url: Optional[str] = Field(default=None)
    status: Status
    rating: Optional[int] = Field(default=None, ge=1, le=5)
    notes: Optional[str] = Field(default=None, max_length=500)
    platform: Platform
    genres: List[GenreEnum]
    release_date: date
    date_completed: Optional[date] = None


class GameRead(BaseModel):
    id: int
    name: str
    cover_url: Optional[str] = Field(default=None)
    status: Status
    rating: Optional[int] = None
    notes: Optional[str] = None
    platform: Platform
    genres: List[str]
    release_date: date
    date_completed: Optional[date] = None


class CreateGame(GameBase):
    pass


class UpdateGame(BaseModel):
    name: Optional[str] = None
    cover_url: Optional[str] = Field(default=None)
    status: Optional[Status] = None
    rating: Optional[int] = Field(default=None, ge=1, le=5)
    notes: Optional[str] = Field(default=None, max_length=500)
    platform: Optional[Platform] = None
    genres: Optional[List[GenreEnum]] = None
    release_date: Optional[date] = None
    date_completed: Optional[date] = None
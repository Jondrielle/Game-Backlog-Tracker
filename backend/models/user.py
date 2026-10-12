from typing import Optional
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
	id: Optional[int] = Field(default=None,primary_key=True)
	firebase_uid: str = Field(unique=True, index=True)
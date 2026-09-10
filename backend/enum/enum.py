from enum import Enum

class Status(str, Enum):
	BACKLOG = "Backlog"
    PLAYING = "Playing"
    COMPLETED = "Completed"
    DROPPED = "Dropped"

class Platform(str, Enum):
	PC = "PC"
    PLAYSTATION = "PlayStation"
    XBOX = "Xbox"
    SWITCH = "Switch"

class Genre(str,Enum):
	ACTION = "Action"
    ADVENTURE = "Adventure"
    RPG = "RPG"
    STRATEGY = "Strategy"
    SIMULATION = "Simulation"
    SPORTS = "Sports"
    RACING = "Racing"
    PUZZLE = "Puzzle"
    HORROR = "Horror"
    PLATFORMER = "Platformer"
    SHOOTER = "Shooter"
    FIGHTING = "Fighting"
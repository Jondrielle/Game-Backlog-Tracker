from sqlmodel import Session, create_engine

DATABASE_URL = "postgresql+psycopg://jondriellewilson@localhost:5432/game_backlog"

engine = create_engine(DATABASE_URL)

def get_session():
	with Session(engine) as session:
		yield session
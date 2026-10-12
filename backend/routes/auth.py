from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import auth as firebase_auth

from sqlmodel import Session, select
from sqlalchemy import delete

from database import get_session
from models.user import User
from models.game import Game, GenreGame

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])
bearer_scheme = HTTPBearer()



def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    session: Session = Depends(get_session),
) -> User:
    try:
        decoded_token = firebase_auth.verify_id_token(credentials.credentials)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = session.exec(
        select(User).where(User.firebase_uid == decoded_token["uid"])
    ).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not registered in database")

    return user


@auth_router.post("/signup")
def register_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    session: Session = Depends(get_session),
):
    try:
        decoded_token = firebase_auth.verify_id_token(credentials.credentials)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    firebase_uid = decoded_token["uid"]

    user = session.exec(
        select(User).where(User.firebase_uid == firebase_uid)
    ).first()

    if user is None:
        user = User(firebase_uid=firebase_uid)
        session.add(user)
        session.commit()
        session.refresh(user)

    return {"id": user.id, "firebase_uid": user.firebase_uid}

@auth_router.post("/signup")
def register_user(current_user: User = Depends(get_current_user)):
    return {"message": "User registered", "user_id": current_user.id}

@auth_router.get("/me")
def read_current_user(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "firebase_uid": current_user.firebase_uid,
    }


@auth_router.delete("/deleteAccount")
def delete_user_account(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    # 1. Delete the Firebase Authentication account.
    try:
        firebase_auth.delete_user(current_user.firebase_uid)
    except Exception:
        raise HTTPException(
            status_code=502,
            detail="Could not delete Firebase account. Database data was preserved.",
        )

    # 2. Find this user's games.
    game_ids = session.exec(
        select(Game.id).where(Game.user_id == current_user.id)
    ).all()

    try:
        # 3. Remove genre links for those games.
        if game_ids:
            session.exec(
                delete(GenreGame).where(
                    GenreGame.game_id.in_(game_ids)
                )
            )

        # 4. Remove this user's games.
        session.exec(
            delete(Game).where(Game.user_id == current_user.id)
        )

        # 5. Remove the PostgreSQL user row.
        session.exec(
            delete(User).where(User.id == current_user.id)
        )

        session.commit()

    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=500,
            detail="Firebase account was deleted, but database cleanup failed.",
        )

    return {"message": "Account and associated game data deleted"}

from sqlalchemy.orm import Session

from models import UserGameAssociations


def get_all_games_or_current_user(db: Session, user_id: int = None):
    if user_id:
        return db.query(UserGameAssociations).filter(UserGameAssociations.user_id == user_id)
    return db.query(UserGameAssociations).all()


def connect_to_game(db: Session, user_id: int = None, game_id: int = None):
    if user_id and game_id:
        check_connection = db.query(UserGameAssociations).filter(
            UserGameAssociations.user_id == user_id).filter(UserGameAssociations.game_id == game_id).first()
        if check_connection:
            return {"Message": "Game is already connected"}
        db.add(UserGameAssociations(user_id=user_id, game_id=game_id))
        db.commit()
        return {"Message": "Connected"}
    return {"Message": "Incorrect data"}
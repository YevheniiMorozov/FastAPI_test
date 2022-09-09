import json
from collections import defaultdict

from fastapi import FastAPI, Response, Depends
from typing import Optional

import crud
from database import engine, Session

app = FastAPI()


def get_db():
    connections = engine.connect()
    db = Session(bind=connections)
    yield db
    db.rollback()
    db.close()


@app.get('/games')
def get_games(user_id: Optional[int] = None, db: Session = Depends(get_db)):
    result = crud.get_all_games_or_current_user(db, user_id=user_id)
    if user_id:
        user = result[0].user
        result_dict = {
            "user": {"id": user.id, "name": user.name, "age": user.age, "email": user.email},
            "games": [{"id": elements.game.id, "name": elements.game.name} for elements in result]
        }
    else:
        result_dict = defaultdict(list)
        for element in result:
            result_dict[element.game.name].append(element.user.name)
    return Response(content=json.dumps(result_dict), media_type="app/json")


@app.post("/connect")
def connect_to_game(user_id: Optional[int] = None, game_id: Optional[int] = None, db: Session = Depends(get_db)):
    result = crud.connect_to_game(db, user_id=user_id, game_id=game_id)
    return Response(content=json.dumps(result), media_type="app/json")

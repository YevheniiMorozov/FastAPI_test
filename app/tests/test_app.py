import pytest
from fastapi import Request
from fastapi.testclient import TestClient
from sqlalchemy import create_engine

from app.database import Session
from app.models import Base, User, Game, UserGameAssociations
from app.main import app, get_db


SQLALCHEMY_DATABASE_URL = POSTGRES_URI = f"postgresql://postgres:pass@localhost/test"


@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    yield engine


@pytest.fixture(scope="function")
def db(db_engine):
    connection = db_engine.connect()

    connection.begin()

    db = Session(bind=connection)

    yield db

    db.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db):
    app.dependency_overrides[get_db] = lambda: db

    with TestClient(app) as c:

        yield c


@pytest.fixture
def add_value(db):
    users = [User(id=1, name="user1", age=1, email='email1'), User(id=2, name="user2", age=2, email='email2')]
    games = [Game(id=1, name='game1'), Game(id=2, name='game2'), Game(id=3, name='game3')]
    db.add_all(users)
    db.commit()
    db.add_all(games)
    db.commit()
    connect_games = [UserGameAssociations(user_id=1, game_id=1), UserGameAssociations(user_id=2, game_id=2)]
    db.add_all(connect_games)
    db.commit()


def test_db(db, add_value):
    user = db.query(User).filter(User.id == 1).first()
    connect = db.query(UserGameAssociations).filter(UserGameAssociations.user_id == 1).first()
    assert user.name == "user1"
    assert user.age == 1
    assert user.email == "email1"
    assert connect.game.name == "game1"


def test_get_games(client, add_value):
    url = app.url_path_for("get_games")
    response = client.get(url)
    assert response.status_code == 200

    data = response.json()
    assert data['game1'] == ['user1']
    assert data['game2'] == ['user2']

    url += "?user_id=1"
    response = client.get(url)
    assert response.status_code == 200

    data = response.json()
    assert data["user"]["name"] == "user1"
    assert data["games"] == [{"id": 1, "name": "game1"}]


def test_connect(client, add_value):
    url = app.url_path_for("connect_to_game")
    response = client.post(url)
    assert response.status_code == 200
    assert response.json() == {"Message": "Incorrect data"}

    url += "?user_id=1&game_id=3"
    response = client.post(url)
    assert response.status_code == 200
    assert response.json() == {"Message": "Connected"}

    response = client.post(url)
    assert response.status_code == 200
    assert response.json() == {"Message": "Game is already connected"}


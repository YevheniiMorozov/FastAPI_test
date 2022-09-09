from sqlalchemy import String, Column, Integer, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    email = Column(String(250), nullable=False, unique=True)


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class UserGameAssociations(Base):
    __tablename__ = "user_game_assoc"

    user_id = Column(ForeignKey(User.id), primary_key=True)
    user = relationship(User)
    game_id = Column(ForeignKey(Game.id), primary_key=True)
    game = relationship(Game)

import random
from string import ascii_letters

from models import User, UserGameAssociations, Game, Base
from database import engine, Session

games = [
    "WoT", "Dota 2", "Counter-Strike: GO", "HoMM3", "Minecraft",
    'Risk of Rain 2', "Terraria", "Disciples", "Witcher", "GTA", "RDR2"
]

usernames = ["Adam", "Jacob", "Ann", "Mary", "Jacob", "Lia"]

user_emails = [f'{"".join(random.choices(population=ascii_letters, k=8))}@gmail.com' for _ in range(6)]

users_list = [User(id=index + 1, name=usernames[index], age=random.randint(0, 100), email=user_emails[index])
              for index in range(6)]

games_list = [Game(id=index + 1, name=games[index]) for index in range(len(games))]


if __name__ == '__main__':
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    with engine.connect() as connection:
        with Session(bind=connection) as session:
            session.add_all(users_list)
            session.commit()
            session.add_all(games_list)
            session.commit()
            assoc_list = []
            for user in users_list:
                for game in random.sample(games_list, random.randint(1, 3)):
                    assoc_list.append(UserGameAssociations(user_id=user.id, game_id=game.id))
            session.add_all(assoc_list)
            session.commit()
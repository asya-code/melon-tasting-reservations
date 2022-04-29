from model import Reservation, User, db
from server import app
import datetime
import os
import crud
import model
import server
from random import choice, randint


os.system("dropdb melon")
os.system("createdb melon")

model.connect_to_db(server.app)
model.db.create_all()

for n in range(10):
    email = f"user{n}@test.com"  # Voila! A unique email!
    password = "test"
    user = crud.create_user(email=email, password=password)    
    model.db.session.add(user)
model.db.session.commit()

# Get users ids:
users = crud.get_users()
users_id = []
for user in users:
    users_id.append(user.user_id)

for n in range(10):
    time = datetime.datetime(2021, 10, n + 1, 9)
    new_reservation = crud.create_reservation(given_user_id=choice(users_id), time=time)
    model.db.session.add(new_reservation)
model.db.session.commit()    
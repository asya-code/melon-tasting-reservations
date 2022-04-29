from datetime import datetime
from flask_sqlalchemy  import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """Users"""
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(25), nullable=False)

    def __repr__(self):
        return f"<User {self.user_id}, email={self.email}"

class Reservation(db.Model):
    """Melon tresting reservation"""
    __tablename__ = "reservations"

    reservation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(25), nullable=False)
    time = db.Column(db.DateTime(timezone=True))

    def __repr__(self):
        return f"<User {self.user_id} has tasting scheduled on {self.time}>"

def connect_to_db(app, db_uri="postgresql:///melon", echo=True):
    """Connect to database."""

    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = app
    db.init_app(app)
    print("Connected to the db!")

if __name__ == "__main__":
    from server import app
    
    connect_to_db(app)

from model import db, User, Reservation
from datetime import datetime

def create_user(email, password):
    """Create and return a new user."""
    user = User(email=email, password=password)
    return user

def get_user_by_email(given_email):
    """Return a user by email."""
    return User.query.filter(User.email == given_email).first()

def get_users():
    return User.query.all()

def create_reservation(given_user_id, time):
    """new reservation"""
    reservation = Reservation(user_id=given_user_id, time=time)
    return reservation

def get_reservations_by_user(given_user_id):
    """Return all reservations made by user"""
    return Reservation.query.filter(Reservation.user_id==given_user_id).all

def get_reservation_by_time_user(given_user_id,time):
    return Reservation.query.get(Reservation.user_id==given_user_id, time==time)
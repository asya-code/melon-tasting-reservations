from flask import Flask, render_template, request, flash, session, redirect, jsonify
from model import connect_to_db, db, User, Reservation
import os
import crud
from jinja2 import StrictUndefined
from dateutil.parser import parse

app = Flask(__name__)
app.sekret_key="dev"
app.jinja_env.undefined = StrictUndefined

@app.route("/")
def homepage():
    """View homepage."""
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Process user login."""
    login_email = request.form.get("email")
    login_password = request.form.get("password")

    if crud.get_user_by_email(login_email):

        user = crud.get_user_by_email(login_email)
        if login_password != user.password:
            flash("Incorrect password. Try again")
        else:
            #add the user's user_id to the flask session
            session['current_user'] = user.user_id
            session['current_email'] = user.email
            #session['current_user_obj'] = user
            flash(f'Logged in as {user.email}')
    else:
        flash("Looks like we don't know you yet! ")
        return redirect("/registration")
    return render_template("make_reservation.html")


@app.route('/logout')
def logout_user():
    """ Log user out, delete their info from the session """

    session['current_user'] = None
    session['current_email'] = None
   # session['current_user_obj'] = None

    flash("You have logged out. Goodbye!")
    return redirect('/')


@app.route("/reservations", methods=["POST", "GET"])
def get_user_reservations():
    """Retrieve reservations the user has made."""
    if request.method == "POST":
        email = request.form.get("email")
        session["current_email"] = email
    else:
        # if the user is not in session, redirect them to the homepage
        if "current_email" in session:
            email = session["current_email"]
        else:
            redirect("/")
    user_id = crud.get_user_by_email(email).user_id
    existing_reservations = Reservation.get_reservations_by_user(user_id)

    return render_template("reservations.html", reservations=existing_reservations)


@app.route("/schedule")
def render_schedule():
    """View scheduling page."""
    return render_template("schedule.html")


@app.route("/reservations/delete", methods=["POST"])
def delete_reservation():
    """Delete reservations the user has made."""
    time = parse(request.form.get("startTime"))
    user_id = session["current_email"].user_id
    reservation_to_delete = crud.get_reservation_by_time_user(user_id,time)
    db.session.delete(reservation_to_delete)
    db.session.commit()
    return jsonify(reservation_to_delete.reservation_id)


@app.route("/reservations/book", methods=["POST"])
def make_reservation():
    """Create a reservation with the specified user and time."""
    reservation_start = parse(request.form.get("start_time"))
    username = session["username"]
    new_reservation = Reservation.new_reservation_for_user(username, reservation_start)
    db.session.add(new_reservation)
    db.session.commit()
    return redirect("/reservations")


@app.route("/search_reservations", methods=["GET"])
def search_reservation():
    start_time = parse(request.args.get("startTime"))
    end_time = parse(request.args.get("endTime"))

    available_times = Reservation.find_available_reservations(
        start_time, end_time, session["username"]
    )
    return jsonify(available_times)



if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
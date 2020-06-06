import os
import sys, json

from flask import Flask, flash, jsonify, redirect, render_template, session, url_for, request
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required
from sqlite import createTables, insertNewUser, selectUserByUsername, getUsersMovies, addMovie, deleteMovie
from media import Movie, searchMovie

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Start DB
createTables()


def getApp():
    return app



# Homepage route ##################################################################################
@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "GET":
        movies = getUsersMovies(session["user_id"])
    
        return render_template('index.html', movies=movies)
    else:
        # User wants to delete movie
        query = request.form.get("movie")
        print(query)

        deleteMovie(query, session["user_id"])
        return redirect("/")
    

# Login routes ####################################################################################
@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Please enter username", 403)
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Please enter password", 403)

        # Query database for username
        rows = selectUserByUsername(request.form.get("username"))

        # Ensure username exists and password is correct, [0][3] is 'hash' column
        if len(rows) != 1 or not check_password_hash(rows[0][3], request.form.get("password")):
            return apology("Invalid username and/or password", 403)

        # Remember which user has logged in, [0][0] is 'id' column
        session["user_id"] = rows[0][0]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


# Logout routes ###################################################################################
@app.route("/logout")
def logout():

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


# Register routes #################################################################################
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Please enter username", 403)

        # Ensure email was submitted
        elif not request.form.get("email"):
            return apology("Please enter email", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Please enter password", 403)

        # Ensure password and password-confimation fields match
        if not request.form.get("password") == request.form.get("confirmation"):
            return apology("Passwords don't match", 403)

        # Check if username is already taken
        row = selectUserByUsername(request.form.get("username"))
        if row:
            return apology("Sorry, that username is already taken", 403)

        # Everything checks out, now hash the password before saving new user
        hashedPass = generate_password_hash(request.form.get("password"), "pbkdf2:sha256", 8)

        # Now store the new user
        insertNewUser(request.form.get("username"), request.form.get("email"), hashedPass)

        # Redirect to home page
        return redirect("/")
    else:
        # GET method
        return render_template("register.html")


# Add Routes ######################################################################################
@app.route("/add", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        query = request.form.get("movie")
        movie = searchMovie(query)
        addMovie(movie, session["user_id"])
        # Redirect to home page
        return redirect("/")
    else:
        # GET method
        return render_template("add.html")


# Error Handling ##################################################################################
def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
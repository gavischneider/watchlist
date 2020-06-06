import sqlite3
#from media import Movie

# Users Database ##################################################################################

# Create tables
def createTables():
    # Define connection and cursor
    connect = sqlite3.connect('watchlist.db')
    cursor = connect.cursor()

    # Create users table
    command1 = """CREATE TABLE IF NOT EXISTS
    users(id INTEGER PRIMARY KEY, username TEXT, email TEXT, hash TEXT)"""

    cursor.execute(command1)

    # Create movies table
    command2 = """CREATE TABLE IF NOT EXISTS
    movies(name TEXT, director TEXT, year INTEGER, artwork TEXT, user_id INTEGER, FOREIGN KEY(user_id) REFERENCES users(id))"""

    cursor.execute(command2)

    connect.commit()
    connect.close()

# Insert new user
def insertNewUser(username, email, hash):
    connect = sqlite3.connect('watchlist.db')
    cursor = connect.cursor()
    cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (None, username, email, hash))
    connect.commit()
    connect.close()

# Select user by username
def selectUserByUsername(username):
    connect = sqlite3.connect('watchlist.db')
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", [username])
    result = cursor.fetchall()
    connect.close()
    return result


# Movies Database #################################################################################

# Get a users list of movies
def getUsersMovies(id):
    connect = sqlite3.connect('watchlist.db')
    cursor = connect.cursor()
    cursor.execute
    cursor.execute("SELECT * FROM movies WHERE user_id=?", [id])
    result = cursor.fetchall()
    connect.close()
    return result

# Add a movie to a users list
def addMovie(movie, id):
    connect = sqlite3.connect('watchlist.db')
    cursor = connect.cursor()
    name = movie.name
    director = movie.director
    year = movie.year
    artwork = movie.artwork
    user_id = id
    cursor.execute("INSERT INTO movies VALUES (?, ?, ?, ?, ?)", (name, director, year, artwork, user_id))
    connect.commit()
    connect.close()

# Delete a movie from a users list
def deleteMovie(movie, user_id):
    connect = sqlite3.connect('watchlist.db')
    cursor = connect.cursor()
    cursor.execute("DELETE FROM movies WHERE user_id=? AND name =?", (user_id, movie))
    connect.commit()
    connect.close()
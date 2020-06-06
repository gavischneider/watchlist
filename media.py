import itunespy

# Define Movie class
class Movie:
  def __init__(self, name, director, year, artwork):
    self.name = name
    self.director = director
    self.year = year
    self.artwork = artwork


###################################################################################################
# Search for movie
def searchMovie(query):
    movies = itunespy.search_movie(query)
    movie = movies[0]
    name = movie.track_name
    director = movie.artist_name
    date = str(movie.release_date)
    year = date[:4]
    artwork = movie.artwork_url_100
    newMovie = Movie(name, director, year, artwork)
    return newMovie



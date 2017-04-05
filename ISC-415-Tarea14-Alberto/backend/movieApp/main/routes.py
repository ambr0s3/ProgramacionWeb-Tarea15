from flask import request, Blueprint
from flask import jsonify
from flask import make_response
from movieApp.data.models import db, Movie, Review
import urllib.request
import os

main = Blueprint('main', __name__, template_folder='templates')

@main.route('movies', methods=["POST"])
def movie_handler():
  if request.method == 'POST':
    data = request.get_json()
    movies = data["movies"]
    for i in range(len(movies)):
      movie = Movie.query.filter_by(name=movies[i]["title"]).first()
      if movie is None:
        if 'poster_path' in movies[i]:
          if movies[i]["poster_path"] is not None:
            posterUrl = "http://image.tmdb.org/t/p/w150" + movies[i]["poster_path"]
            localUrl = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + '\client\static\images\\' + str(movies[i]["id"]) + ".jpg"
            urllib.request.urlretrieve(posterUrl, localUrl)
            movie = Movie(movies[i]["id"], movies[i]["title"], movies[i]["overview"], movies[i]["poster_path"])
          else:
            movie = Movie(movies[i]["id"], movies[i]["title"], movies[i]["overview"], None)
          db.session.add(movie)
          db.session.commit()
  return "Done"

@main.route('movies/search/', methods=["GET"])
def movies_search_handler():
  if request.method == 'GET':
    query = request.args.get('query')
    movies = Movie.query.filter(Movie.name.like(query+"%")).all()
    movies = [movie.serialize() for movie in movies]
    return jsonify(movies)

@main.route('movies/all/', methods=["GET"])
def movies_all_handler():
  if request.method == 'GET':
    movies = Movie.query.all()
    movies = [movie.__dict__ for movie in movies]
    return jsonify(movies)


@main.route('reviews', methods=["POST"])
def reviews_handler():
  if request.method == 'POST':
    data = request.form.to_dict()
    if "title" and "description" and "rating" and "user" and "device_id" not in data:
      print("MISSING A FIELD!")
      resp = make_response("Missing Data", 404)
    else:
      print("LOOKING FOR MOVIE!!")
      movie = Movie.query.filter_by(name=data["title"]).first()
      print(movie)
      if movie is not None:
          movie = movie.serialize()
          review = Review(movie["id"], data["description"], data["rating"], data["user"], data["device_id"])
          db.session.add(review)
          db.session.commit()
          resp = make_response("", 200)
      else:
        resp = make_response("Movie does not exist", 404)
    return resp

@main.route('movies/reviewed', methods=["GET"])
def movies_reviewed_handler():
  if request.method == 'GET':
    movies = Movie.query.all()
    movies = [movie.serialize() for movie in movies]
    movies_reviewed = [movie for movie in movies if len(movie["reviews"]) > 0]
    print(movies_reviewed)
    for movie in movies_reviewed:
      counter = 0
      acum = 0
      for review in movie["reviews"]:
        counter = counter + 1
        acum = acum + review["rating"]
      avg = acum / counter
      movie["average"] = avg
    return jsonify(movies_reviewed)

@main.route('reviews/<movie>', methods=["GET"])
def reviews_by_movie_handler(movie):
  if request.method == 'GET':
    movie = Movie.query.filter_by(name=movie).first()
    movie = movie.serialize()
    reviews = movie["reviews"]
    return jsonify(reviews)
import flask
import requests
import random
import json
import os
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

def get_movie_info():
    TMDB_BASE_URL = "https://api.themoviedb.org/3"
    TMDB_MOVIE_LIST_PATH = ["/movie/634649", "/movie/361743", "/movie/324786", "/movie/263115"]
    TMDB_MOVIE_PATH = random.choice(TMDB_MOVIE_LIST_PATH)

    movie_response = requests.get(
        TMDB_BASE_URL + TMDB_MOVIE_PATH,
        params={
        "api_key": os.getenv("TMDB_API_KEY"),
        },
    )

    movie_info = movie_response.json()

    global MOVIE_NAME; MOVIE_NAME = movie_info["title"]
    global MOVIE_TAGLINE; MOVIE_TAGLINE = movie_info["tagline"]
    global MOVIE_POSTER_PATH; MOVIE_POSTER_PATH = movie_info["poster_path"]
    global MOVIE_BACKDROP_PATH; MOVIE_BACKDROP_PATH = movie_info["backdrop_path"]
    global MOVIE_OVERVIEW; MOVIE_OVERVIEW = movie_info["overview"]
    global MOVIE_BACKDROP_IMAGE; MOVIE_BACKDROP_IMAGE = get_movie_backdrop(MOVIE_BACKDROP_PATH)
    global MOVIE_POSTER_IMAGE; MOVIE_POSTER_IMAGE = get_movie_poster(MOVIE_POSTER_PATH)
    global MOVIE_GENRES; MOVIE_GENRES = [genre["name"] for genre in movie_info["genres"]]
    global MOVIE_WIKI_LINK; MOVIE_WIKI_LINK = get_wiki_link(MOVIE_NAME)

def get_movie_poster(MOVIE_POSTER_PATH):
    TMDB_MOVIE_POSTER_BASE_URL = "https://image.tmdb.org/t/p"
    POSTER_SIZE = "/w342"

    return TMDB_MOVIE_POSTER_BASE_URL + POSTER_SIZE + MOVIE_POSTER_PATH

def get_movie_backdrop(MOVIE_BACKDROP_PATH):
    TMDB_MOVIE_POSTER_BASE_URL = "https://image.tmdb.org/t/p"
    POSTER_SIZE = "/original"

    return TMDB_MOVIE_POSTER_BASE_URL + POSTER_SIZE + MOVIE_BACKDROP_PATH

def get_wiki_link(MOVIE_NAME):
    WIKI_BASE_URL = "https://www.wikipedia.org/w/api.php"

    wiki_response = requests.get(
        WIKI_BASE_URL,

        params={
        "action": "query",
        "prop": "info",
        "inprop": "url",
        "format": "json",
        "titles": MOVIE_NAME,
        },
    )

    wiki_link = wiki_response.json()["query"]["pages"][
        list(wiki_response.json()["query"]["pages"])[0]]["fullurl"]
    
    return wiki_link

app = flask.Flask(__name__)
app.secret_key = os.getenv("SUPER_SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    comments = db.relationship('Comment', backref='author', lazy=True)

    def __repr__(self) -> str:
        return f"Person with username: {self.username}"
    
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self) -> str:
        return '<Comment %r' % self.username
    
    
with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return flask.render_template("login.html")

@app.route("/login", methods=["POST", "GET"])
def login_user():
    if flask.request.method == "POST":
        form_data_login = flask.request.form
        login_username = form_data_login["username"]
        if (check_username(login_username)):
            return flask.redirect(flask.url_for("home_page"))
        else:
            flask.flash("User not found")
            return flask.render_template("login.html")
    else:
        return flask.render_template("login.html")
    
def check_username(username):
    return User.query.filter_by(username=username).first()


@app.route("/signup", methods=["POST", "GET"])
def signup_user():
    if flask.request.method == "POST":
        form_data_signup = flask.request.form
        signup_username = form_data_signup["username"]
        user = User(username=signup_username)
        if (check_username(signup_username)):
            flask.flash("This username has been used. Try a different one")
            return flask.render_template("signup.html")
        else:
            db.session.add(user)
            db.session.commit()
            flask.flash("You have successfully signed up. Please login to continue.")
            return flask.redirect(flask.url_for("login_user"))

    else:
        return flask.render_template("signup.html")
    

@app.route("/home", methods=["POST", "GET"])
def home_page():
    get_movie_info()
    return flask.render_template("moviediscovery.html",
        TITLE = MOVIE_NAME, TAGLINE = MOVIE_TAGLINE, GENRES = MOVIE_GENRES, POSTER = MOVIE_POSTER_IMAGE,
        WIKI = MOVIE_WIKI_LINK, BACKDROP = MOVIE_BACKDROP_IMAGE, OVERVIEW = MOVIE_OVERVIEW)

app.run(debug=True)

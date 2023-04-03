import flask
import requests
import random
import json
import os
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

@app.route("/")
def index():
    get_movie_info()
    return flask.render_template("moviediscovery.html",
        TITLE = MOVIE_NAME,
        TAGLINE = MOVIE_TAGLINE,
        GENRES = MOVIE_GENRES,
        POSTER = MOVIE_POSTER_IMAGE,
        WIKI = MOVIE_WIKI_LINK,
        BACKDROP = MOVIE_BACKDROP_IMAGE,
        OVERVIEW = MOVIE_OVERVIEW
        )

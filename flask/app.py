from flask import Flask, request, redirect, url_for, session, g, flash, \
render_template
import requests
import time
import urllib
import json
from pymongo import MongoClient

#Connect to MovieDetector database and user collection
client = MongoClient()
db = client.MovieDetector


from flask_oauthlib.client import OAuth, OAuthException
# <<<<<<< HEAD
# #from flask_oauth import OAuth
# =======
# from sqlalchemy import create_engine, Column, Integer, String
# from sqlalchemy.orm import scoped_session, sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
# import flask_oauthlib
# >>>>>>> 3f5f33a7f8f50875ad8714d83dd94fd939c02b8b
#https://pythonhosted.org/Flask-OAuth/
#^ All log-in tutorial
FACEBOOK_APP_ID = '???'
FACEBOOK_APP_SECRET = '???'

app = Flask(__name__)
app.debug = True
app.secret_key = 'MovieDetector'
oauth = OAuth(app)

facebook = oauth.remote_app(
    'facebook',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'email'},
    base_url='https://graph.facebook.com',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    access_token_method='GET',
    authorize_url='https://www.facebook.com/dialog/oauth'
)

api_key = 'fa03116693262062589d14a72cc612d0'
api_url = 'https://api.themoviedb.org/3/'


class Movie:
    def __init__(self, title, poster, popularity, release_date, overview):
        self.title = title
        self.poster = poster
        self.popularity = popularity
        self.release_date = release_date
        self.overview = overview
        self.myRating = 0


def get_json(url):
    '''Returns json text from a URL'''
    response = None
    try:
        response = urllib.request.urlopen(url)
        json_text = response.read().decode(encoding = 'utf-8')
        return json.loads(json_text)
    finally:
        if response != None:
            response.close()

@app.route("/", methods = ['GET','POST'])
def index():
    return render_template("welcome.html")

@app.route('/login')
def login():
    callback = url_for(
        'facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True
    )
    return facebook.authorize(callback=callback)

@app.route('/login/authorized')
def facebook_authorized():
    resp = facebook.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    if isinstance(resp, OAuthException):
        return 'Access denied: %s' % resp.message

    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me')
    return 'Logged in as id=%s name=%s redirect=%s' % \
        (me.data['id'], me.data['name'], request.args.get('next'))


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')

#https://developers.themoviedb.org/3/search/search-movies
#https://stackoverflow.com/questions/14152276/themoviedb-json-api-with-jquery
#search example
@app.route('/test', methods=['GET','POST'])
def detect():
    if request.method == 'POST':
        result = request.form['title']

        url = 'https://api.themoviedb.org/3/search/movie?api_key=fa03116693262062589d14a72cc612d0&page=1&query=' + result.replace(" ", "%20")
        img_url = 'https://image.tmdb.org/t/p/w500'
        movie_list = get_json(url)
        movies = []
        for i in movie_list['results']:
            movies.append(Movie(i['title'],
                                img_url + i['poster_path'],
                                i['popularity'],
                                i['release_date'],
                                i['overview']))
        return render_template("test.html", movies = movies, listnum = len(movies))
    else:
        return render_template("test.html")

"""
def detect():
    if request.method == 'POST':

        result = request.form['id']

        url = "https://api.themoviedb.org/3/movie/" + result + "?api_key=fa03116693262062589d14a72cc612d0"

        #url = "https://api.themoviedb.org/3/movie/343611?api_key=fa03116693262062589d14a72cc612d0"

        response = urllib.request.urlopen(url)
        data = json.loads(response.read())
        ret = ''
        ret = ret + "<h1>Title: "
        ret = ret + str(data.get(u'title')) + "</h1>"
        ret = ret + "<h1>Poster: "#just try(Delete if not working)
        ret = ret + 'https://image.tmdb.org/t/p/w500' + str(data.get(u'poster_path')) + "</h1>"#just try(Delete if not working)
        ret = ret + "<h2>"
        ret = ret + str(data.get(u'tagline')) + "</h2>"
        ret = ret + "<h3>Overview: "
        ret = ret + str(data.get(u'overview')) + "</h3>"
        ret = ret + "<h2>Release Date: "
        ret = ret + str(data.get(u'release_date')) + "</h2>"
        return ret
    else:
        return  render_template("test.html")
"""



if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, request, redirect, url_for, session, g, flash, \
render_template
import requests
import time
import urllib
import json
import pymongo
from pymongo import MongoClient

'''Connect to MovieDetector database'''
client = MongoClient()
db = client.users


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

FACEBOOK_APP_ID = '2094967570803709'
FACEBOOK_APP_SECRET = '8463d71df35e3d004f3cd087a520c2d0'

app = Flask(__name__)
app.debug = True
app.secret_key = 'MovieDetector'
oauth = OAuth(app)

facebook = oauth.remote_app(
    'facebook',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'public_profile,email'},
    base_url='https://graph.facebook.com',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    access_token_method='GET',
    authorize_url='https://www.facebook.com/dialog/oauth'
)

api_key = 'fa03116693262062589d14a72cc612d0'
api_url = 'https://api.themoviedb.org/3/'


class Movie:
    def __init__(self, title, poster, id, release_date, overview):
        self.title = title
        self.poster = poster
        self.id = id
        self.release_date = release_date
        self.overview = overview
        self.myRating = 0


def get_json(url):
    '''Returns json text from a URL '''
    response = None
    try:
        response = requests.get(url)
        json_data = json.loads(response.text)
        return json_data
    finally:
        if response != None:
            response.close()

@app.route("/", methods = ['GET','POST'])
def index():
    return render_template("index.html")

'''Route to get movie search keyword from user'''
@app.route('/search', methods=['GET','POST'])
def search():
    return render_template("search.html")

'''Route to display search results and allow user to select movie'''
@app.route('/results', methods = ['GET','POST'])
def results():
    if request.method == 'POST':
        print("THIS IS THE POST REQUEST")
        keyword = request.form['movie_search']
        url = 'https://api.themoviedb.org/3/search/movie?api_key=fa03116693262062589d14a72cc612d0&page=1&query=' + keyword
        img_url = 'https://image.tmdb.org/t/p/w500'
        movie_list = get_json(url)
        movie_results = movie_list['results']
    return render_template("results.html", movie_results = movie_results)


@app.route('/login')
def login():
    callback = url_for(
        'facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True
    )
    return facebook.authorize(callback=callback)

@app.route('/logout')
def logout():
    session.pop('log-in',None)
    session.pop('oauth_token', None)
    session.pop('id', None)
    session.pop('name', None)
    return redirect(url_for('index'))

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
    me = facebook.get('/me?fields=id,name')
    session["log-in"] = True
    session["id"] = str(me.data['id'])
    session["name"] = str(me.data['name'])
    flash('Logged in as ' + str(me.data['name']))
    return redirect(url_for('index'))


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

        url = 'https://api.themoviedb.org/3/search/movie?api_key=fa03116693262062589d14a72cc612d0&page=1&query=' + (result.replace(":", "%3A")).replace(" ", "%20")
        img_url = 'https://image.tmdb.org/t/p/w500'
        movie_list = get_json(url)
        movies = []
        for i in movie_list['results']:
            movies.append(Movie(i['title'],
                                img_url + i['poster_path'],
                                i['id'],
                                i['release_date'],
                                i['overview']))
        return render_template("test.html", movies = movies, listnum = len(movies))
    else:
        return render_template("test.html")

"""
@app.route('/test', methods=['GET','POST'])
def detect(id):
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
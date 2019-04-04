from flask import Flask, request, render_template
import requests
import time
import urllib, json

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/test', methods=['GET','POST'])
def detect():
    if request.method == 'POST':
        response = request.form['id']
        r = requests.get("https://api.themoviedb.org/3/movie/" + str(response) + "?api_key=fa03116693262062589d14a72cc612d0")
        s = r.json()
        output = []
        movies = s['title']['release_date']
        for i in range(len(movies)):
            output += [movies[i]['title']]
        return render_template('test.html', x=output)
    else:
        return render_template('test.html')

"""
def search(id):
    url = "https://api.themoviedb.org/3/movie/" + str(id) + "?api_key=fa03116693262062589d14a72cc612d0"

#I need .request here if you guy have to delete it out, please do.
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    ret = ''
    ret = ret + str(data.get(u'title')) + "\n"
    ret = ret + str(data.get(u'tagline')) + "\n"
    ret = ret + str(data.get(u'id')) + "\n"
    ret = ret + str(data.get(u'overview')) + "\n"
    ret = ret + str(data.get(u'release_date'))
    print(ret)

search(343611)
search(297802)
"""
if __name__ == "__main__":
    app.run()
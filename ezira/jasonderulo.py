import urllib, json

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

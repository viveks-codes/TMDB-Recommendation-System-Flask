from flask import Flask, flash, redirect, render_template, \
     request, url_for
import pandas as pd 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# import os
import requests, lxml
from bs4 import BeautifulSoup

cv = CountVectorizer(max_features=8000,stop_words='english')

df = pd.read_csv('finalPrep.csv')
tags = pd.read_csv('tags.csv')
vector = cv.fit_transform(tags['tags']).toarray()


similarity = cosine_similarity(vector)
counter = 0
#
# for i in movienames:
#     # print(len(movienstaticames) - counter )
#     # bd.download(i+" Movie", limit=1, output_dir='static/photos', timeout=10, verbose=False)
#     # counter+=1
#     #if file exist skip else download 
#     if os.path.isfile('static/photos/'+i+' Movie.jpg'):
#         counter+=1
#         print('file exist, {}'.format(counter))
#     else:
#         bd.download(i+" Movie", limit=1, output_dir='static/photos', timeout=10, verbose=False)
#         counter+=1
#         print('file downloaded, {}'.format(counter))


def rec(movie,n):
    r = []
    index = tags[tags['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
    for i in distances[:int(n)+1]:
        r.append(tags.iloc[i[0]].title)
    return r
#id	genres	keywords	title	overview	crew	budget	homepage	release_date
def get_details(movie):
    index = df[df['title'] == movie].index[0]
    key = df.iloc[index]['keywords']
    crew = df.iloc[index]['crew']
    budget = df.iloc[index]['budget']
    homepage = df.iloc[index]['homepage']
    release_date = df.iloc[index]['release_date']
    genres = df.iloc[index]['genres']
    return key,crew,budget,homepage,release_date,genres
def google_image_search_link(keyword):
    l = []
    for i in keyword:
        count = 0
        #get high quality image
        url = "https://www.google.com/search?q="+i +"movie hd wallpaper&sxsrf=APq-WBtENMmC6vZtak_ak8672vI7NyLBtw:1649785953438&tbm=isch&source=iu&ictx=1&vet=1&fir=EjtSrMTdwp5H1M%252CUHUPOmPGfyBCqM%252C%252Fm%252F0bth54&usg=AI4_-kRJ5y2Aeeis8RRyLjuNnR05eRaK0A&sa=X&ved=2ahUKEwjb49bNi4_3AhW2wosBHXG6BgsQ_B16BAgJEAI"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content, 'lxml')
        #get only one image link from the search result
        for img in soup.find_all('img'):
         if img.get('src')[0:4] == 'http':
             l.append(img.get('src'))
             count+=1
             if count == 1:
                 break
    return l
app = Flask(__name__)
@app.route('/')

def index():
    return render_template('b.html',df=df['title'],links=google_image_search_link(['Avatar']),suggestions=rec(df['title'][0],5))

@app.route('/recommend',methods=['GET','POST'])
def recommend():
    movie = request.form['movie']
    n = request.form['n']
    # print(rec(movie,n))
    suggestions = rec(movie,int(n))
    links = google_image_search_link(suggestions)
    overview = df[df['title'] == movie]['overview'].values[0]
    #print(links)
    key,crew,budget,homepage,release_date,genres = get_details(movie)
    #get image links of suggestions from google image search 
    return render_template('index.html',df=df['title'],linkssuggestionzip=zip(suggestions,links),n=n,movie=movie,overview=overview,suggestions=suggestions,links=links,key=key,crew=crew,budget=budget,homepage=homepage,release_date=release_date,genres=genres)

if __name__ == '__main__':
    app.run()

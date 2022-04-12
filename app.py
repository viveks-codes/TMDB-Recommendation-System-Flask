from flask import Flask, flash, redirect, render_template, \
     request, url_for
import pandas as pd 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# import os
import requests, lxml, 
from bs4 import BeautifulSoup

cv = CountVectorizer(max_features=8000,stop_words='english')

df = pd.read_csv('finalPrep.csv')

vector = cv.fit_transform(df['tags']).toarray()


similarity = cosine_similarity(vector)
counter = 0

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
    index = df[df['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
    for i in distances[1:int(n)+1]:
        r.append(df.iloc[i[0]].title)
    return r
def google_image_search_link(keyword):
    l = []
    for i in keyword:
        count = 0
        url = 'https://www.google.com/search?q='+i+' Movie&source=lnms&tbm=isch'
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
    return render_template('index.html',df=df['title'])

@app.route('/recommend',methods=['GET','POST'])
def recommend():
    movie = request.form['movie']
    n = request.form['n']
    # print(rec(movie,n))
    suggestions = rec(movie,int(n))
    links = google_image_search_link(suggestions)
    #print(links)
    #get image links of suggestions from google image search 
    return render_template('index.html',df=df['title'],linkssuggestionzip=zip(suggestions,links),n=n,movie=movie)

if __name__ == '__main__':
    app.run(debug=False)

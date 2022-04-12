from flask import Flask, flash, redirect, render_template, \
     request, url_for
import pandas as pd 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
from bing_image_downloader import downloader as bd

cv = CountVectorizer(max_features=8000,stop_words='english')

df = pd.read_csv('finalPrep.csv')

vector = cv.fit_transform(df['tags']).toarray()


similarity = cosine_similarity(vector)
    
def rec(movie,n):
    r = []
    index = df[df['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
    for i in distances[1:int(n)+1]:
        r.append(df.iloc[i[0]].title)
    return r
    
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
    return render_template('index.html',suggestions=suggestions,df=df['title'])

if __name__ == '__main__':
    app.run(debug=False)

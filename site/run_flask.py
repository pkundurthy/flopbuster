from contextlib import closing
from flask import Flask, render_template, request, redirect
import os
from flopbuster import site

app = Flask(__name__)
# app.debug = True
# host = 'http://www.flopbuster.com/'

@app.route("/")
def hello(name=None):
    return render_template('index.html',name=name)

@app.route("/about")
def about(name=None):
    return render_template('about.html',name=name)

@app.route("/slides")
def about(name=None):
    return render_template('slides.html',name=name)

@app.route("/app")
def toapp(name=None):
    return render_template('app.html',name=name)

@app.route('/app', methods=['POST'])
def myrun_search():
    search_term = request.form['text']
    MovieData = site.compileMovieData(search_term)
    Actual,Predict,Budget = site.MovieComparison(search_term)
    grossInfo = ['$'+Actual,'$'+Predict,'$'+Budget]
    DInfo = ', '.join(MovieData['Director(s)'])
    AInfo = ', '.join(MovieData['Actor(s)'])
    WInfo = ', '.join(MovieData['Writer(s)'])
    GInfo = ', '.join(MovieData['Genre'])
    return render_template('results.html',\
             InfoSet=[search_term,GInfo,DInfo,AInfo,WInfo],gross=grossInfo)

if __name__ == "__main__":
    app.run('0.0.0.0', port=80)
    # run locally
    # app.debug = True
    app.run()
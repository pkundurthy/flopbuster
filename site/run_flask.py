from contextlib import closing
from flask import Flask, render_template, request
import os
from flopbuster import site
import socket

app = Flask(__name__)
app.debug = True

@app.route("/")
def hello(name=None):
    return render_template('index.html',name=name)

@app.route("/about")
def about(name=None):
    return render_template('about.html',name=name)

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
    return render_template('results.html', InfoSet=[search_term,GInfo,DInfo,AInfo,WInfo],gross=grossInfo)

if __name__ == "__main__":
    app.debug = True
    app.run(port=80)
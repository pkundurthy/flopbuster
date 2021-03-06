from contextlib import closing
from flask import Flask, render_template, request, redirect
import os
from flopbuster import site
import socket

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
def slides(name=None):
    return render_template('slides.html',name=name)

@app.route("/charts")
def charts(name=None):
    return render_template('charts.html',name=name)

@app.route("/app")
def toapp(name=None):
    return render_template('app.html',name=name)

@app.route('/app', methods=['POST'])
def myrun_search():
    search_term = request.form['text']
    MovieData = site.compileMovieData(search_term)
    Actual,Predict,Budget = site.MovieComparison(search_term)
    grossInfo = [Actual,Predict,Budget]
    DInfo = ', '.join(MovieData['Director(s)'])
    AInfo = ', '.join(MovieData['Actor(s)'])
    WInfo = ', '.join(MovieData['Writer(s)'])
    GInfo = ', '.join(MovieData['Genre'])
    site.generate_chart(MovieData,search_term)
    site.generate_bar_chart(Actual,Predict,Budget)
    return render_template('results.html',\
             InfoSet=[search_term,GInfo,DInfo,AInfo,WInfo],gross=grossInfo)

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE or Chrome,
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

if __name__ == "__main__":
    
    if socket.gethostbyname(socket.gethostname()).startswith('172.'):
        address = '0.0.0.0'
        portNum = 80
        app.debug = True
    else:
        address = '127.0.0.1'
        portNum = 5000
        app.debug = True

    app.run(address, port=portNum)
    # run locally

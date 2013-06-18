from contextlib import closing
from flask import Flask, render_template, request
import os
import flopbuster


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
    results  = flopbuster.readdb.grabMovieComparison(search_term)
    out = results
    return render_template('results.html', post_links=out)


if __name__ == "__main__":
    app.debug = True
    app.run()
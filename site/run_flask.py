from contextlib import closing
from flask import Flask, render_template
import os

#app = Flask(__name__, template_folder=tmpl_dir)

app = Flask(__name__)

app.debug = True

@app.route("/")
def hello(name=None):
    return render_template('index.html',name=name)

@app.route("/about")
def about(name=None):
    return render_template('about.html',name=name)
    
if __name__ == "__main__":
    app.run()
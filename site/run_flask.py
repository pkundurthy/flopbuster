from contextlib import closing
from flask import Flask, render_template, request
import os
import cPickle
import unicodedata

#app = Flask(__name__, template_folder=tmpl_dir)
oFile = open('templates/OutDict.pickle','rb')
#oFile = open('OutDict.pickle','rb')
ResultsDict = cPickle.load(oFile)

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
    results  = flopbuster.movie.grabMovieComparison(search_term)
    out = results
    return render_template('results.html', post_links=out)


def getSucessString(sNumber):

    sNumber = long(sNumber)
    if sNumber == -1:
        oStr = 'Fail!'
    elif sNumber == 0:
        oStr = '(meh) was ok...'
    elif sNumber == 1:
        oStr = 'Good!'
    elif sNumber == 2:
        oStr = 'Awesome! $$'
    else:
        oStr = 'Unknown'

    return oStr

def grabMovieComparison(movieName):

    # print movieName, ResultsDict
    mName = unicodedata.normalize('NFKD', movieName).encode('ascii','ignore')

    ActualSucess = flopbuster.movie.getSucessString(ResultsDict[mName]['Actual'])
    PredictedSucess = flopbuster.movie.getSucessString(ResultsDict[mName]['Predicted'])

    # return [mName,ResultsDict[mName]['Actual'],ResultsDict[mName]['Predicted']]
    return [mName,ActualSucess,PredictedSucess]

# @app.route("/js_barchart")
# def toapp(name=None):
#     return render_template('js_barchart.html',name=name)


if __name__ == "__main__":
    app.debug = True
    app.run()
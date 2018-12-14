from flask import Flask, render_template, redirect
import pandas as pd
from flask_pymongo import PyMongo
from bson.json_util import dumps
from flask_cors import CORS 

app = Flask(__name__)
CORS(app)

app.config["MONGO_URI"] = "mongodb://heroku_sjm9g8xc:4mvq9ej8mp5hlvqdqbgc53d2bf@ds017678.mlab.com:17678/heroku_sjm9g8xc"

mongo = PyMongo(app)

@app.route('/twitter')
def twitter_data():
    scraped = mongo.db.twitter.find()
    scrape = dumps(scraped)
    return scrape

@app.route('/polls')
def aprove_data():
    scraped2 = mongo.db.polls.find()
    scrape2 = dumps(scraped2)
    return scrape2

@app.route('/compare')
def compare_data():
<<<<<<< HEAD
    scraped3 = mongo.db.compare.find()
=======
    scraped3 = mongo.db.trump_twitter.find()
>>>>>>> 4b2ccbe668071d318bd4558dd6b2d13ba3e3369d
    scrape3 = dumps(scraped3)
    return scrape3


@app.route('/')
def main():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

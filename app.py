from flask import Flask, render_template, redirect
import pandas as pd
from flask_pymongo import PyMongo
from bson.json_util import dumps
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config["MONGO_URI"] = "mongodb://localhost:27017/Stuff"

mongo = PyMongo(app)

@app.route('/twitter')
def twitter_data():
    scraped = mongo.db.trump_twitter.find({})
    scrape = dumps(scraped)
    return scrape

@app.route('/approve')
def aprove_data():
    data = pd.read_csv("https://projects.fivethirtyeight.com/trump-approval-data/approval_polllist.csv")
    data["enddate"] = pd.to_datetime(data["enddate"].values, infer_datetime_format=True)
    data2 = data.set_index("enddate").groupby(pd.TimeGrouper("W")).mean()
    data3 = data2.reset_index()
    dat = data3.to_json(orient = "records")
    return dat

@app.route('/')
def main():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

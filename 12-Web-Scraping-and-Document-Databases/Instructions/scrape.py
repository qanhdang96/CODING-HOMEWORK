from flask import Flask, render_template, redirect
from flask_pymongo import pymongo
import scrape_mars

app = Flask(__name__)

conn = "mongodb://localhost:27017/mission_to_mars"
client = pymongo.MongoClient(conn)

@app.route("/")
def home():
    mars_info = client.db.mars_info.find_one()
    return render_template("index.html", mars_info = mars_info)

@app.route("/scrape")
def scrape_route():
    mars_info = client.db.mars_info
    mars_data = scrape_mars.scrape()
    mars_info.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
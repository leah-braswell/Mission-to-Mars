#use flask to render a template
from flask import Flask, render_template
#use PyMongo to interact with mongo db
from flask_pymongo import PyMongo 
import scraping

#set up the flask app
app = Flask(__name__)

#Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#define route for HTML page
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template('index.html', mars=mars)

#define the scraping route
@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scraping.scrape_all()
    mars.update({}, mars_data, upsert=True)
    return "Scraping Successful"

#tell flask to run
if __name__ == '__main__':
    app.run()


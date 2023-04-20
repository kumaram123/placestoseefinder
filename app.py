import sqlite3
from flask import Flask, render_template, request, redirect
from werkzeug.exceptions import abort
import cache
import json
import readTree

app = Flask(__name__)

@app.route('/')
def index():

    with open('state_names.json') as f:
        states = json.load(f)

    form_data = {
        'states': states,
        'cat_dict': readTree.tree_txt_to_dict()
    }

    return render_template('index.html', data=form_data)

@app.route('/invalid')
def invalid_search_term():
    return render_template('invalid.html')

# get user entry from website form and show resulting tourist spots
@app.route('/tourist_spots_results', methods = ['POST', 'GET'])
def data():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        form_data = request.form

        user_search_state = form_data["State"]
        user_search_location = form_data["Location"].title()
        user_search_category = form_data["Category"].lower()

        # perform web scraping on yelp and get API data from Yelp Fusion
        info, isValid, location_title = cache.getCache(user_search_location, user_search_category)

        if isValid == False:
            return redirect("/invalid")

        else:
            data = {'location': user_search_location, 'state': user_search_state, 'category': user_search_category.title(), 'tourist_spot_info': info, 'pageTitle' : location_title}

            return render_template('touristspots.html', data=data, form_data = form_data)
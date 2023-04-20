# SI 507 Final Project

## __Project:__ Places to Visit Recommender
### __By:__ Anu Kumar

This program uses the API provided by Yelp Fusion. To obtain a Yelp Fusion API key, use this link: https://www.yelp.com/fusion. Create a file named :bulb:proj_secrets.py:bulb: and enter the line: :exclamation:MY_API_KEY = 'your_yelpfusion_api_key':exclamation: into the file to support the program.

__Required Python packages:__ requests, flask and bs4.

The "Places to Visit Recommender" is a Flask application with an easy-to-use user interface. On the homepage, the user can enter a "State", "City", and "Category" for which they would like to see results for using the dropdown and search bars. After submitting the search form, the app redirects to the next page, which shows all the top rated places to see based on the user's search. Users can see a list of the top rated places to see, along with additional details about each place, such as:
* Image of the place
* Average Rating (out of 5)
* Number of Ratings Given
* Phone Number
* Link to Yelp to see more details about the place


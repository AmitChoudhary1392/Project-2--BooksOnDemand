# import necessary libraries
import os
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)
import requests

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################

from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://xuogxhiwjayrke:c8a1bc208e9b818bfa20e9e23ee06c5fe8857d6becc336912a42184706764b3b@ec2-184-72-236-3.compute-1.amazonaws.com:5432/d2ma2m4n786kvk"
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgres:root123@localhost:5432/BookShare')
db = SQLAlchemy(app)

from models import *

bookTitle=""

# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")

#navigation route
@app.route("/bookSearch", methods=["GET", "POST"])
def GetForm():
    
    return render_template("booksearch.html")    

# Query the database and send the jsonified results
@app.route("/getBook", methods=["GET", "POST"])
def getBook():
    if request.method == "POST":
        global bookTitle 
        bookTitle = request.form["title"]
        return redirect("/showBooks") 


# Query the database and send the jsonified results
@app.route("/showBooks")
def showBooks():
   
    global bookTitle
    #data = requests.get(f"/api/findbook/{bookTitle}")
    return redirect(f"/api/findbook/{bookTitle}")


@app.route("/api/findbook/<searchTerm>")
def findbook(searchTerm):

    # Google developer API key
    from config import api_key

    params={'maxResults':1}

    url= f'https://www.googleapis.com/books/v1/volumes?q={searchTerm}&key={api_key}'
    response = requests.get(url, params).json()

    results=response['items']

    books=[]

    for item in results:
        try:
            book={
                'id_book': item['id'],
                'title':item['volumeInfo']['title'] if 'title' in item['volumeInfo'].keys() else " ",
                'description': item['volumeInfo']['description'] if 'description' in item['volumeInfo'].keys() else " ",
                'isbn':item['volumeInfo']['industryIdentifiers'][0]['identifier'] if 'industryIdentifiers' in item['volumeInfo'].keys() else " ",
                'authors':item['volumeInfo']['authors'] if 'authors' in item['volumeInfo'].keys() else " ",
                'language':item['volumeInfo']['language'] if 'language' in item['volumeInfo'].keys() else " ",
                'image_url':item['volumeInfo']['imageLinks']['smallThumbnail'] if 'imageLinks' in item['volumeInfo'].keys() else " ",
                'publisher': item['volumeInfo']['publisher'] if 'publisher' in item['volumeInfo'].keys() else " ",        
                'published_date':item['volumeInfo']['publishedDate'] if 'published_date' in item['volumeInfo'].keys() else " "
            }
            
        except:
            book = {'id_book': 'not found'}
        
        books.append(book)
        
        bookrecord = Book(id_book= book['id_book'], title=book['title'], description= book['description'], isbn= book['isbn'], author=book['authors'], language=book['language'],
                            image_url=book['image_url'], publisher=book['publisher'], published_date=book['published_date'])
        db.session.add(bookrecord)
        db.session.commit()

    return jsonify(books)
#######################################################################################


#################################################
# bookshare page and Owner Details
#################################################

#navigation route
@app.route("/bookShare", methods=["GET", "POST"])
def Shareform():
    
    return render_template("bookshare.html")

# Query the database and send the jsonified results
@app.route("/send", methods=["GET", "POST"])
def send():
    if request.method == "POST":
        title = request.form["title"]
        owner_email = request.form["email"]
        rating = request.form["rating"]
        review= request.form["review"]
        location= request.form["location"]

        owner = Owner(title=title, owner_email=owner_email, rating=rating, review=review, location=location)
        #db.session.add(owner)
        #db.session.commit()
        return redirect("/", code=302)

    #return render_template("form.html")


""" @app.route("/api/ownerdetails")
def owner():
    results = db.session.query(Pet.name, Pet.lat, Pet.lon).all()

    hover_text = [result[0] for result in results]
    lat = [result[1] for result in results]
    lon = [result[2] for result in results]

    pet_data = [{
        "type": "scattergeo",
        "locationmode": "USA-states",
        "lat": lat,
        "lon": lon,
        "text": hover_text,
        "hoverinfo": "text",
        "marker": {
            "size": 50,
            "line": {
                "color": "rgb(8,8,8)",
                "width": 1
            },
        }
    }]

    return jsonify(pet_data) """


if __name__ == "__main__":
    app.run()

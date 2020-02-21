# import necessary libraries
import os
import numpy as np
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

# global variables used in the code
bookTitle=""
books=[]
books_owner=[]

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
        
        bookTitle = request.form["title"]
        #print(bookTitle)
        
        books_db = db.session.query(Book.id_book, Book.title, Book.image_url).filter(Book.title.like(f'%{bookTitle}%')).all()

        #print (books_db)
        global books
        books=[]
        for book in books_db:
            dict_book = {
                "id" : book.id_book,
                "Title" : book.title,
                "image_url": book.image_url   
            }
            books.append(dict_book)

            
    return render_template("bookresults.html")
    
 
#route for JAVASCRIPT connection to display results table for user
@app.route("/api/findbook")
def findbook():

    global books
    data= jsonify(books)
    return data
    

#######################################################################################


#################################################################################################################
# ###################         bookshare page and Owner Details    #################################################
###################################################################################################################

#navigation route
@app.route("/bookShare", methods=["GET", "POST"])
def Shareform():
    
    return render_template("bookshare.html")

#get search results for selection by owner
@app.route("/getBook_owner", methods=["GET", "POST"])
def getBook_owner():
    if request.method == "POST":
        
        bookTitle = request.form["title"]

    #Googlebooks API connection
    from config import api_key

    params={'maxResults':2}

    url= f'https://www.googleapis.com/books/v1/volumes?q={bookTitle}&key={api_key}'
    response = requests.get(url, params).json()

    global books_owner
    books_owner=[]
    
    #Extracting required information from Google books API
    results=response['items']
    for item in results:
        try:
            book={
                'image_url':item['volumeInfo']['imageLinks']['smallThumbnail'] if 'imageLinks' in item['volumeInfo'].keys() else " ",
                'id_book': item['id'],
                'title':item['volumeInfo']['title'] if 'title' in item['volumeInfo'].keys() else " ",
                'category/genre':item['volumeInfo']['categories'] if 'categories' in item['volumeInfo'].keys() else " ",
                'authors':item['volumeInfo']['authors'] if 'authors' in item['volumeInfo'].keys() else " ",
                'description': item['volumeInfo']['description'] if 'description' in item['volumeInfo'].keys() else " ",
                'isbn':item['volumeInfo']['industryIdentifiers'][0]['identifier'] if 'industryIdentifiers' in item['volumeInfo'].keys() else " ",
                'language':item['volumeInfo']['language'] if 'language' in item['volumeInfo'].keys() else " ",
                'published_date':item['volumeInfo']['publishedDate'] if 'published_date' in item['volumeInfo'].keys() else " ",
                'publisher': item['volumeInfo']['publisher'] if 'publisher' in item['volumeInfo'].keys() else " "     
            }
            
        except:
            book = {'id_book': 'not found'}
    
        books_owner.append(book)

            
    return render_template("shareresults.html")

@app.route("/api/findbook_owner")
def findbook_owner():

    global books_owner
    dict_books=[]
    
    for book in books_owner:
            dict_book = {
                "id" : book['id_book'],
                "Title" : book['title'],
                "image_url": book['image_url']   
            }
            dict_books.append(dict_book)
    
    data= jsonify(dict_books)
    return data

#navigation route
@app.route("/OwnerDetails")
def OwnerDetails():

    return render_template('OwnerDetails.html')

#complete book details
@app.route("/api/findSharedBook/<id>")
def findSharedBook(id):
    
    books = db.session.query(Book.id_book, Book.title, Book.description, Book.isbn,
                            Book.author, Book.language, Book.image_url, Book.publisher,
                            Book.published_date).filter(Book.id_book == id).first()

    owners = db.session.query(Owner.owner_email, Owner.rating, Owner.review, Owner.location,
                            Owner.lat, Owner.lon, Owner.contact_details, 
                            Owner.available).filter(Owner.id_book == id).all()

    listOwners = []
    for owner in owners:
        dict_owner = {
            "email:" : owner.owner_email,
            "rating" : owner.rating,
            "review": owner.review,
            "location": owner.location,
            "lat" : owner.lat,
            "lon" : owner.lon,
            "contact_details": owner.contact_details,
            "available": owner.available   
        }
        listOwners.append(dict_owner)


    book_data = [{
        "Id": books[0],
        "Title": books[1],
        "Description": books[2],
        "ISBN": books[3],
        "Authors": books[4],
        "Language": books[5],
        "Image_URL" : books[6],
        "Publisher" : books[7],
        "Publication_Date": books[8],
        "Owners": listOwners
    }]
    print (book_data)

    return jsonify(book_data)

# Query the database and send the jsonified results
@app.route("/send", methods=["GET", "POST"])
def send():
    
    if request.method == "POST":
        title = request.form["title"]
        owner_email = request.form["email"]
        rating = request.form["rating"]
        review= request.form["review"]
        location= request.form["location"]
        contact_details= request.form["contact_details"]
        available= request.form["available"]

        from config import api_key
        params={'address':location,
                "key":api_key}

        url= 'https://maps.googleapis.com/maps/api/geocode/json?'
        response=requests.get(url, params).json()

        # getting lat/lng for the given address
        lat =response['results'][0]['geometry']['location']['lat']
        lon =response['results'][0]['geometry']['location']['lng']


###*** need to modify the owner table fields in database
        owner = Owner(id_book= np.random.randint(100),owner_email=owner_email, rating=rating, review=review, location=location, lat=lat, lon=lon, contact_details=contact_details,
        available=available)
        global db
        db.session.add(owner)
        db.session.commit()
    return redirect("/", code=302)
    print("*********************************")
    #return render_template("form.html")

    
@app.route("/api/ownerdetails/<location>")
def owner(location):

    

    """ results = db.session.query(Pet.name, Pet.lat, Pet.lon).all()

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
    }] """

    return jsonify(pet_data)


if __name__ == "__main__":
    app.run()

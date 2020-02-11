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
books=[]
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

    from config import api_key

    params={'maxResults':5}

    url= f'https://www.googleapis.com/books/v1/volumes?q={bookTitle}&key={api_key}'
    response = requests.get(url, params).json()
    global books
    books=[]
    results=response['items']
    for item in results:
        try:
            book={'id_book': item['id'],
              'title':item['volumeInfo']['title'] if 'title' in item['volumeInfo'].keys() else " ",
              'description': item['volumeInfo']['description'] if 'description' in item['volumeInfo'].keys() else " ",
              'isbn':item['volumeInfo']['industryIdentifiers'][0]['identifier'] if 'industryIdentifiers' in item['volumeInfo'].keys() else " ",
              'author':item['volumeInfo']['authors'] if 'authors' in item['volumeInfo'].keys() else " ",
              'language':item['volumeInfo']['language'] if 'language' in item['volumeInfo'].keys() else " ",
              'image_url':item['volumeInfo']['imageLinks']['smallThumbnail'] if 'imageLinks' in item['volumeInfo'].keys() else " ",
              'publisher': item['volumeInfo']['publisher'] if 'publisher' in item['volumeInfo'].keys() else " ",        
              'published_date':item['volumeInfo']['publishedDate'] if 'published_date' in item['volumeInfo'].keys() else " "
            }
            
        except:
            book = {'id_book': 'not found'}
    
        books.append(book)
        #bookrecord = Book(id_book= book['id_book'], title=book['title'], description= book['description'], isbn= book['isbn'], author=book['authors'], language=book['language'],
                        #image_url=book['image_url'], publisher=book['publisher'], published_date=book['published_date'])
    
    #####need a conditional to check the book already in database, no duplicates??????
        #db.session.add(bookrecord)
        #db.session.commit()
            
    return render_template("bookresults.html")
    
 

# Query the database and send the jsonified results
""" @app.route("/showBooks")
def showBooks():
   
    global bookTitle
    #data= requests.get(f"/api/findbook/{bookTitle}")
    return redirect(f"/api/findbook/{bookTitle}")
 """

@app.route("/api/findbook")
def findbook():

    global books
    data= jsonify(books)
    return data
    
    """ results = db.session.query(Book.image_url, Book.id_book, Book.title, Book.author, Book.description,Book.isbn, Book.language, Book.published_date,
                                Book.publisher).all()
    return jsonify(results) """
    """ for image_url, id_book, title, author, description,isbn, language,published_date,publisher in results:
        book={}
        book['image_url']=image_url
        book['id_book']=id_book
        book['title']=title
        book['authors']=author
        book['description']= description
        book['isbn']= isbn
        book['language']=language
        book['published_date']=published_date
        book['publisher']=publisher  
        books.append(book)
    return jsonify(books) """
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

        from config import api_key
        params={'address':location,
                "key":api_key}

        url= 'https://maps.googleapis.com/maps/api/geocode/json?'
        response=requests.get(url, params).json()

        # getting lat/lng for the given address
        lat =response['results'][0]['geometry']['location']['lat']
        lng =response['results'][0]['geometry']['location']['lng']


###*** need to modify the owner table fields in database
        #owner = Owner(title=title, owner_email=owner_email, rating=rating, review=review, location=location)
        #db.session.add(owner)
        #db.session.commit()
    return redirect("/", code=302)
    print("*********************************")
    #return render_template("form.html")


#################################################
# bookshare return data from Database
#################################################

@app.route("/api/listSharedBooks")
def listSharedBooks():
    books = db.session.query(Book.id_book, Book.title, Book.image_url).all()

    listBooks = []
    for book in books:
        dict_book = {
            "id:" : book.id_book,
            "Title" : book.title,
            "image_url": book.image_url   
        }
        listBooks.append(dict_book)

    return jsonify(listBooks)

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

    return jsonify(book_data)


if __name__ == "__main__":
    app.run()

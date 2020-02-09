import os
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

import requests

app = Flask(__name__)

bookTitle = ""

from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://xuogxhiwjayrke:c8a1bc208e9b818bfa20e9e23ee06c5fe8857d6becc336912a42184706764b3b@ec2-184-72-236-3.compute-1.amazonaws.com:5432/d2ma2m4n786kvk"
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '')

db = SQLAlchemy(app)

from models import *


# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/Shareform", methods=["GET", "POST"])
def Shareform():
    
    return render_template("Shareform.html")

@app.route("/GetForm", methods=["GET", "POST"])
def GetForm():
    
    return render_template("GetForm.html")

# Query the database and send the jsonified results
@app.route("/getBook", methods=["GET", "POST"])
def getBook():
    if request.method == "POST":
        global bookTitle 
        bookTitle = request.form("bookName")
        return redirect("/showBooks") 


# Query the database and send the jsonified results
@app.route("/showBooks")
def showBooks():
   
    global bookTitle
    data = requests.get(f"/api/findbook/{bookTitle}")
    return render_template('ShareForm.html',data=data)


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

    return jsonify(books)

if __name__ == "__main__":
    app.run()

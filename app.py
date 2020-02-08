import os
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or "sqlite:///db.sqlite"
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '')

db = SQLAlchemy(app)

from .models import Books
from .models import Owner


# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")


# Query the database and send the jsonified results
@app.route("/send", methods=["GET", "POST"])
def send():
    if request.method == "POST":
        #assigning variables entered from the form
        #[""] is the name of the input element in the form html
        
        idBook = request.form["id"]
        ownerEmail = request.form["bookName"]
        rating = request.form["bookName"]
        review = request.form["bookName"]
        postalCode = request.form["bookAuthor"]
        contactDetail = request.form["book"]
        available = request.form["book"]
        
        #assign class variables to Owner object     
        bookShare = Owner(id_book=idBook, owner_email=ownerEmail, rating=rating, review=review, 
                postal_code=postalCode, contact_details=contactDetail, available=available)
        
        #add the book record to database
        db.session.add(bookShare)
        
        #commit
        db.session.commit()
        
        #return back to index page 'landing page'
        return redirect("/", code=302)

    #return render template on the form page
    return render_template("form.html")


@app.route("/api/findbook")
def pals():
    #again we will need the db name and the column names to assign it to results
    results = db.session.query(Pet.name, Pet.lat, Pet.lon).all()
    
    

    
    bookName = [result[0] for result in results]
    postalCode = [results[1] for result in results]
    secondarrayobj = [result[1] for result in results]
    thirdarrayobj = [result[2] for result in results]
    lat 
    lng


    book_data = [{
        "type": "Feature",
        "properties": {
            "name": bookName,
            "popupContent": f'{bookName} is here'     
        },
        "geometry":{
            "type": "Point",
            "cooridnates": [lat,lng]
           } 
        }]
        
          

    return jsonify(book_data)


if __name__ == "__main__":
    app.run()

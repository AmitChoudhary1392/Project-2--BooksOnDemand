from .app import db


class Books(db.Model):
    __tablename__ = 'Book'

    id_book = db.Column(db.String(20), primary_key=True) 
    title = db.Column(db.String(300))
    description = db.Column(db.String(5000))
    isbn = db.Column(db.String(13))
    image_url = db.Column(db.String(1000))
    authors = db.Column(db.String(200))
    publication_date = db.Column(db.Date)
    publisher = db.Column(db.String(100))
    language = db.Column(db.String(2))

    def __repr__(self):
        return '<Book %r>' % (self.title)


class Owner(db.Model):
    __tablename__ = 'Owner'

    id_book = db.Column(db.String(20), primary_key=True) 
    owner_email = db.Column(db.String(60), primary_key=True)
    rating = db.Column(db.Integer)
    review = db.Column(db.String(1000))
    postal_code = db.Column(db.String(6))
    contact_details = db.Column(db.String(1000))
    available = db.Column(db.Integer)

    def __repr__(self):
        return '<Owner %r>' % (self.owner_email)

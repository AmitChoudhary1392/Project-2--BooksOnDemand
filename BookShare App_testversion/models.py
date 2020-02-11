from app import db


class Book(db.Model):
    __tablename__ = 'Book'

    id_book = db.Column(db.String(20), primary_key=True) 
    title = db.Column(db.String(300))
    description = db.Column(db.String(5000))
    isbn = db.Column(db.String(13))
    image_url = db.Column(db.String(1000))
    author = db.Column(db.String(500))
    published_date = db.Column(db.String(10))
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
    location = db.Column(db.String(150))
    lat= db.Column(db.Float(10))
    lng= db.Column(db.Float(10))
    contact_details = db.Column(db.String(1000))
    available = db.Column(db.Integer)

    def __repr__(self):
        return '<Owner %r>' % (self.owner_email)
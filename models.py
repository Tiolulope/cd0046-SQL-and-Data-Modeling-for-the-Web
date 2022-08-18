# from datetime import datetime
# from email.policy import default
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
from config import *



class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable = False)
    city = db.Column(db.String(120), nullable = False)
    state = db.Column(db.String(120), nullable= False)
    address = db.Column(db.String(120), nullable= False)
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    #here is the mising field for venues
    genres = db.Column(db.String(120), nullable = False)
    # website_link = db.Column(db.String(120), nullable = False)
    website = db.Column(db.String(120), nullable = True)
    seeking_talent = db.Column(db.Boolean, nullable = False)
    seeking_description = db.Column(db.String, nullable = True )
    image_link = db.Column(db.String, nullable = False)
    shows = db.relationship('Show', backref='venue', lazy=True)

    def __repr__(self):
        return f'<Venue {self.id} {self.name}>'


class Artist(db.Model):

    __tablename__ = 'artist'

    id =  db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable = False)
    city = db.Column(db.String(120), nullable= False)
    state = db.Column(db.String(120), nullable = False)
    phone = db.Column(db.String(120), nullable = False)
    genres = db.Column(db.String(120), nullable = False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

# TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
  #here is the missing field for artist
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String())
    shows = db.relationship('Show', backref='artist', lazy=True)
    
    # website = db.Column(db.String(120))
    # seeking_talent = db.Column(db.Boolean, nullable= False, default=True)
    # shows = db.relationship('Show', backref='artist', lazy=True)
    # seeking_description = db.Column(db.String, nullable= True)
    # address = db.Column(db.String(120), nullable = False)

    def __repr__(self):
        return f'<Artist id: {self.id} ,Artist name: {self.name}>'

class Show(db.Model):

    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable = False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<Venue {self.id}>'
    
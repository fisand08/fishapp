from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.bin import get_random_color # import of self-coded routine

"""
Definition of DB
    - Classes correspond to tables
"""

class User(UserMixin, db.Model):  # inherts from db.Model, the bas lass for all models in SQLAlhemy
    # also inhertis from UserMixin from flask-login covering the required functions is_authenticated, is_ative is_anonymus and get_id()
    """
    - Each field is assigned a type or type hint
    - mapped_column provides additional configuration; e.g. if it's unique or indexed
    - "unique" modified gives error if values is added twice to DB
    """
    
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,  unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)

    """
    Relationship to new class Portfolio "author" object; so.relationship() is model class that represents the other side of the relationship;
    the "back_populates" arguments reference the name of the relationship attribute on the other side
    """

    """
    - password hash is used instead of password to not store them as plain text if DB is comprimised
    - optional typing allows empty or "None"
    - from werkzeug, password hashing and it's checking are added as methods
    """
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc))


    def __repr__(self):
        """
        - Tells python how to print objets of this class (e.g. good for debugging)
        """
        return '<User {}>'.format(self.username)
    

@login.user_loader  # user loader is registered with decorator
def load_user(id):
    """
    - flask-login needs to know about the DB, user is loaded via id
    """
    return db.session.get(User, int(id)) # needs to be converted to int as string 


class Water(db.Model):
    # __bind_key__ = 'local_db'
    __tablename__ = 'Water'

    water_id = db.Column(db.Integer, primary_key=True)
    water_name = db.Column(db.String(1024))
    water_type = db.Column(db.String(1024))
    water_country = db.Column(db.String(1024))
    water_region = db.Column(db.String(1024))
    water_owner_id = db.Column(db.Integer, primary_key=True) 
    schongebiet = db.Column(db.Boolean)

    def __repr__(self):
        return f'Water {self.water_id}'


class Water_Coords(db.Model):
    # __bind_key__ = 'local_db'
    __tablename__ = 'Water_Coords'

    water_id = db.Column(db.Integer, primary_key=True)
    coord = db.Column(db.Float)

    def __repr__(self):
        return f'Error {self.error_idx} submitted by {self.submitting_user} at {self.submission.date}'


class Water_Owners(db.Model):
    # __bind_key__ = 'local_db'
    __tablename__ = 'Water_Owners'

    Owner_ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(1024))
    Surname = db.Column(db.String(1024))
    Address_Street = db.Column(db.String(1024))
    Address_PLZ = db.Column(db.Integer)
    Address_City = db.Column(db.String(1024))
    Address_Country = db.Column(db.String(1024))

    def __repr__(self):
        return f'Error {self.error_idx} submitted by {self.submitting_user} at {self.submission.date}'

class Water_Season(db.Model):
    # __bind_key__ = 'local_db'
    __tablename__ = 'Water_Season'

    Saison_ID = db.Column(db.Integer, primary_key=True)
    Saison_From = db.Column(db.DateTime)
    Saison_To = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'Error {self.error_idx} submitted by {self.submitting_user} at {self.submission.date}'


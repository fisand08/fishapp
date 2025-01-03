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


class WATER(db.Model):
    # __bind_key__ = 'local_db'
    __tablename__ = 'Water'

    WATER_ID = db.Column(db.Integer, primary_key=True)
    WATER_NAME = db.Column(db.String(1024))
    WATER_TYPE = db.Column(db.String(1024))
    WATER_COUNTRY = db.Column(db.String(1024))
    WATER_REGION = db.Column(db.String(1024))
    WATER_OWNER_ID = db.Column(db.Integer) 
    SCHONGEBIET = db.Column(db.Boolean)
    WATER_SEASON_ID = db.Column(db.Integer)
    FREIANGELEI = db.Column(db.Boolean)
    FREIANGELEI_INT = db.Column(db.Integer)

    def __repr__(self):
        return f'Water {self.water_id}'


class WATER_COORDS(db.Model):
    # __bind_key__ = 'local_db'
    __tablename__ = 'Water_Coords'

    COORD_ID = db.Column(db.Integer, primary_key=True)
    WATER_ID = db.Column(db.Integer)
    COORD_X = db.Column(db.Float)
    COORD_Y = db.Column(db.Float)

    def __repr__(self):
        return f'water_id {self.water_id}'


class WATER_OWNERS(db.Model):
    # __bind_key__ = 'local_db'
    __tablename__ = 'Water_Owners'

    OWNER_ID = db.Column(db.Integer, primary_key=True)
    OWNER_NAME = db.Column(db.String(1024))
    OWNER_STREET = db.Column(db.String(1024))
    OWNER_PLZ = db.Column(db.Integer)
    OWNER_CITY = db.Column(db.String(1024))
    OWNER_COUNTRY = db.Column(db.String(1024))
    OWNER_PUBLIC = db.Column(db.Boolean)
    OWNER_PUBLIC_INT = db.Column(db.Integer)

    def __repr__(self):
        return f'Owner {self.OWNER_ID}'


class WATER_SEASON(db.Model):
    # __bind_key__ = 'local_db'
    __tablename__ = 'Water_Season'

    SAISON_ID = db.Column(db.Integer, primary_key=True)
    SAISON_FROM = db.Column(db.DateTime)
    SAISON_TO = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'Season {self.SAISON_ID}'


class FISHES(db.Model):
    __tablename__ = 'FISHES'

    FISH_ID = db.Column(db.Integer, primary_key=True)
    FISH_NAME = db.Column(db.String(1024))

    def __repr__(self):
        return f'Owner {self.FISH_ID}'
    
    
class CATCHES(db.Model):
    __tablename__ = 'FISHES'

    CATCH_ID = db.Column(db.Integer, primary_key=True)
    WATER_ID = db.Column(db.Integer)
    CATCH_FISH_ID = db.Column(db.Integer)
    CATCH_LENGTH = db.Column(db.Float)
    CATCH_PIC_PATH = db.Column(db.String(1024))

    def __repr__(self):
        return f'Owner {self.CATCH_ID}'
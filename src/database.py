from flask_sqlalchemy import SQLAlchemy
from enum import Enum
from flask_login import UserMixin

db = SQLAlchemy()

class Weekday(Enum):
    Monday = "Monday"
    Tuesday = "Tuesday"
    Wednesday = "Wednesday"
    Thursday = "Thursday"
    Friday = "Friday"
    Saturday = "Saturday"
    Sunday = "Sunday"

class Channel(db.Model):
    __tablename__ = 'channels'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    programs = db.relationship('Program', back_populates='channel', cascade='all, delete', order_by='Program.start_time')

class Program(db.Model):
    __tablename__ = 'programs'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    start_time = db.Column(db.Time)
    weekday = db.Column(db.Enum(Weekday))
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id', ondelete='CASCADE'))
    channel = db.relationship('Channel', back_populates='programs')

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True)
    name = db.Column(db.String)
    password = db.Column(db.String)
    is_superuser = db.Column(db.Boolean)
    
    def is_active(self):
       return True


def db_init(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
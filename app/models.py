from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Hero(db.Model):
    __tablename__ = 'hero'
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String)
    super_name=db.Column(db.String)
    hero_power=db.relationship('HeroPower',backref='hero')
class HeroPower(db.Model):
    __tablename__='heropower'
    id = db.Column(db.Integer,primary_key=True)
    strength=db.Column(db.String())
    power_id =db.Column(db.Integer(),db.ForeignKey('power.id'))
    hero_id = db.Column(db.Integer(),db.ForeignKey('hero.id'))

class Power(db.Model):
    __tablename__='power'
    id = db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String())
    description=db.Column(db.String(20))
    hero_power=db.relationship('HeroPower',backref='power')


# add any models you may need. 
from random import randint,choice as rc
from faker import Faker
import random
from app import app
from models import db,Hero,Power,HeroPower
fake=Faker()
with app.app_context():
    Hero.query.delete()
    HeroPower.query.delete()
    Power.query.delete()
    heroes=[]
    for i in range(20):
        b=Hero(
            name=fake.first_name(),
            super_name=fake.name()
        )
        heroes.append(b)
    db.session.add_all(heroes)
    heropowers=[]
    for i in range(20):
        strengths=['Weak','Strong','Average']
        m=HeroPower(
            strength=rc(strengths),
            power_id=random.randint(1,20),
            hero_id=random.randint(1,20)

        )
        heropowers.append(m)
        db.session.add_all(heropowers)
    powers=[]
    for i in range(20):
        n=Power(
            name=fake.first_name(),
            description=fake.text(),    
        )
        powers.append(n)
        db.session.add_all(powers)
        db.session.commit()

    
    

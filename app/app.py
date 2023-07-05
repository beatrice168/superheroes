#!/usr/bin/env python3

from flask import Flask, make_response,jsonify,request
from flask_migrate import Migrate

from models import db, Hero,Power,HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return ''
@app.route('/heroes')
def heroes():
    heroes=[]
    for hero in Hero.query.all():
        hero_dict={
             "id":hero.id,
            "name":hero.name,
        }
        heroes.append(hero_dict)
        response=make_response(
            jsonify(heroes),
            200
        )
    return response
@app.route('/heroes/<int:id>')
def hero_by_id(id):
    if id:
        hero=Hero.query.filter_by(id=id).first()
        if hero:
            hero_data={
            "id":hero.id,
            "name":hero.name,
            'powers': [
                {
                    'id': hero_power.power.id,
                    'name': hero_power.power.name,
                    'description': hero_power.power.description
                }
                for hero_power in hero.hero_power
            ]
            }
            response=make_response(
              jsonify(hero_data),
              200
            )
        # response.headers['content-Type']='application/json'
            return response
        else:
            # Return the error JSON response with appropriate HTTP status code
            return {
                'error': 'Hero not found'

            }, 404
@app.route('/powers')
def powerss():
    powers=[]
    for power in Power.query.all():
        power_dict={
            "id":power.id,
            "name":power.name,
            "description":power.description
        }
        powers.append(power_dict)
        response=make_response(
            jsonify(powers),
            200
        )
    return response


@app.route('/powers/<int:id>',methods=['GET','PATCH'])
def powers(id):
    if request.method=='GET':
        power=Power.query.filter_by(id=id).first()
        if power:
            power_data={
            "id":power.id,
            "name":power.name,
            "description":power.description
            }
            response=make_response(
              jsonify(power_data),
              200
            )
        return response
    if request.method == 'PATCH':
        power = Power.query.filter_by(id=id).first()
        if power:
            description = request.form.get('description')
            if description and len(description) < 20:
                response_dict = {
                    "errors": ["validation errors"]
                }
                response = make_response(jsonify(response_dict), 400)
                return response
            for attr in request.form:
                setattr(power, attr, request.form.get(attr))
            # db.session.add(power)
                db.session.commit()

            response_body = {
                "description": "updated description"
            }
            response = make_response(jsonify(response_body), 200)
            return response
        else:
            response = {'error': 'Power not found'}
            return make_response(jsonify(response), 404)

@app.route('/hero_powers',methods=['GET','POST'])
def hero_powers():
    if request.method == 'GET':
       hero_power=[]
       for heropower in HeroPower.query.all():
           hero_dict={
                "id":heropower.id,
                "strength":heropower.strength,
                "hero_id":heropower.hero_id,
                "power_id":heropower.power_id,
           }
           hero_power.append(hero_dict)
           response=make_response(
               jsonify(hero_power),
               200
           )
       return response
    elif request.method == 'POST':
        valid_strengths = ["Strong", "Weak", "Average"]
        data = request.get_json()
        strength = data.get('strength')
        power_id = data.get('power_id')
        hero_id = data.get('hero_id')
        if strength not in valid_strengths:
            response_dict = {
                "errors": ["validation errors"]
            }
            return make_response(jsonify(response_dict), 400)
        if strength and power_id and hero_id:
            hero = Hero.query.get(hero_id)
            power = Power.query.get(power_id)
            if hero and power:
                hero_power_entry = HeroPower(
                    strength=request.form.get("strength"),
                    power_id=request.form.get("power_id"),
                    hero_id=request.form.get("hero_id")
                )
                db.session.add(hero_power_entry)
                db.session.commit()
                hero_data = {
                    "id": hero.id,
                    "name": hero.name,
                    "super_name": hero.super_name,
                    'powers': [
                                 {
                    'id': hero_power.power.id,
                    'name': hero_power.power.name,
                    'description': hero_power.power.description
                    }
                     for hero_power in hero.hero_power
                    ]
                }
                response = make_response(jsonify(hero_data), 201)
                return response
            else:
                response_dict = {
                    "error": "Invalid hero_id or power_id"
                }
                response = make_response(jsonify(response_dict), 404)
                return response
        else:
            response_dict = {
                "error": "Missing required fields"
            }
            response = make_response(jsonify(response_dict), 400)
            return response


if __name__ == '__main__':
    app.run()
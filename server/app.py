#!/usr/bin/env python3
from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        """Get all plants"""
        plants = Plant.query.all()
        return jsonify([plant.to_dict() for plant in plants])

    def post(self):
        """Create a new plant"""
        data = request.get_json()
        new_plant = Plant(
            name=data.get('name'),
            image=data.get('image'),
            price=data.get('price')
        )
        db.session.add(new_plant)
        db.session.commit()
        return make_response(jsonify(new_plant.to_dict()), 201)

class PlantByID(Resource):
    def get(self, plant_id):
        """Get a plant by ID"""
        plant = Plant.query.get_or_404(plant_id)
        return jsonify(plant.to_dict())

    def put(self, plant_id):
        """Update a plant by ID"""
        plant = Plant.query.get_or_404(plant_id)
        data = request.get_json()
        
        plant.name = data.get('name', plant.name)
        plant.image = data.get('image', plant.image)
        plant.price = data.get('price', plant.price)
        
        db.session.commit()
        return jsonify(plant.to_dict())

    def delete(self, plant_id):
        """Delete a plant by ID"""
        plant = Plant.query.get_or_404(plant_id)
        db.session.delete(plant)
        db.session.commit()
        return make_response(jsonify({"message": "Plant deleted"}), 204)

# Register the resources with the API
api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:plant_id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)

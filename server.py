#Flask
from flask import Flask
from flask import request
from flask import Response
from flask import make_response
from flask_restful import reqparse, abort, Api, Resource

# Pymongo for MongoDB
import pymongo

#JSON & BSON
import json
from bson.json_util import dumps
from bson.objectid import ObjectId

#Define DB client
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mongoDemo"]

app = Flask(__name__)
api = Api(app)

#Cars CRUD
class Cars(Resource):
    # /cars GET method
    # Returns array in JSON format with all results (without ObjectId)
    def get(self):
        try:
            carsArray = []
            for x in mydb.Cars.find({},{ "_id": 0, "name": 1, "address": 1, "production_year": 1, "price": 1, "vin_number": 1 }):
                carsArray.append(x)
            return Response(json.dumps(carsArray),  mimetype='application/json', status=201)
        except Exception as e:
            return dumps({'error' : str(e)})

class Car(Resource):
    # /car/<vin> GET method
    # Returns one result matching VIN parameter from request in JSON format
    def get(self, vin):
        try:
            data = mydb.Cars.find_one({'vin_number' : vin},{ "_id": 0, "name": 1, "address": 1, "production_year": 1, "price": 1, "vin_number": 1 })
            return Response(json.dumps(data),  mimetype='application/json', status=201)
        except Exception as e:
            return dumps({'error' : str(e)})

    # /car POST method
    # Body of request must have name, production_year, price and vin_number
    # If new car is added, you will get Success 201 response, or Error exception
    def post(self):
            try:
                data = json.loads(request.data)
                car_name = data['name']
                car_year = data['production_year']
                car_price = data['price']
                car_vin = data['vin_number']
                if car_name and car_year:
                    result = mydb.Cars.insert_one({
                        "name" : car_name,
                        "production_year" : car_year,
                        "price" : car_price,
                        "vin_number" : car_vin
                    })
                #print ( Car.get(result.inserted_id) )
                return "Success", 201
            except Exception as e:
                return dumps({'error' : str(e)})


# API resource routing here
api.add_resource(Cars, '/cars')
api.add_resource(Car, '/car/<vin>')

app.run(debug=True)
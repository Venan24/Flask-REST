#Flask
from flask import Flask
from flask import request
from flask import Response
from flask import make_response

# Pymongo for MongoDB
import pymongo

#JSON & BSON
from bson.json_util import dumps, loads
from bson.objectid import ObjectId

#Define DB client
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mongoDemo"]

app = Flask(__name__)


# /cars GET method
# Returns array in JSON format with all results
@app.route('/cars', methods=['GET'])
def getAllCars():
    try:
        carsArray = mydb.Cars.find({})
        return Response(dumps(carsArray),  mimetype='application/json', status=201)
    except Exception as e:
        return dumps({'error' : str(e)})

# /cars/<vin>
# Returns one result matching VIN parameter from request in JSON format
@app.route('/cars/<vin>', methods=['GET'])
def getCarByVin(vin):
    try:
        ### Find By Object ID mydb.Cars.find_one({'_id' : ObjectId(vin)})
        data = mydb.Cars.find_one({'vin_number' : vin})
        return Response(dumps(data),  mimetype='application/json', status=201)
    except Exception as e:
        return dumps({'error' : str(e)})

# /cars POST
# Body of request must have name, production_year, price and vin_number
# If new car is added, it will be returned in JSON format
@app.route('/cars', methods=['POST'])
def createNewCar():
    try:
        newCarData = loads(request.data)
        if newCarData:
            existingVin = mydb.Cars.find_one({'vin_number' : newCarData['vin_number']})
            if existingVin:
                return Response(dumps({"error:" : "Car with this VIN number already exist"}),  mimetype='application/json', status=400)
            else:
                mydb.Cars.insert_one(newCarData)
                return Response(dumps(newCarData),  mimetype='application/json', status=201)
    except Exception as e:
        return dumps({'error' : str(e)})

app.run(debug=True)
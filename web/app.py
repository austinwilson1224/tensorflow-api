# todo
from flask import Flask,request,jsonify
from flask_restful import Api,Resource

from pymongo import MongoClient

import bcrypt
import requests
import subprocess
import json


# api and app
app = Flask(__name__)
api = Api(app)

# database 
client = MongoClient('mongodb://db:27017')
db = client.ImageRegocnition
users = db.Users 




# this function will search the db for the given username and 
# return true if the count is not zero, i.e. there is at least one user
def userExists(username):
    return users.find({"username":username}).count() != 0

# verify if the encrypted password is correct 
def verifyPw(username,password):
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
    stored_pw = users.find({
        "username":username
    })[0]['passowrd']
    return hashed_pw == stored_pw

# registration post 
class Register(Resource):
    def post(self):
        postedData = request.get_json()
        username = postedData['username']
        password = postedData['password']
        if userExists(username):
            return jsonify({
                "status": 301,
                "message": "username already in use"
            })

        hashed_pw = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
        users.insert({
            "username":username,
            "password":hashed_pw,
            "tokens": 4
        })
        return jsonify({
            "status":200,
            "message":"new user created"
        })

# classify post
class Classify(Resource):
    def post(self):
        postedData = request.get_json()
        username = postedData['username']
        password = postedData['password']
        url = postedData['url']

class Refill(Resource):
    def post(self):
        postedData = request.get_json()
        username = postedData['username']
        admin_pw = postedData['admin_pw']
        refill_amount = postedData['refill_amount']

        # if the user doesn't exist reutn 301 and exit

        # if the password is incorrect return 302 and exit

        # if we make it here then do the comparison




@app.route('/')
def hello():
    return "hello"

api.add_resource(Register,'/register')
api.add_resource(Classify,'/classify')
api.add_resource(Refill,'/refill')



if __name__ == "__main__":
    app.run('0.0.0.0')
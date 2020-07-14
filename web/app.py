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
    # first make sure the user exists
    if not userExists(username):
        return False
    
    hashed_pw = users.find({
        "username":username
    })[0]['passowrd']
    return hashed_pw == bcrypt.hashpw(password.encode('utf8'),hashed_pw)


def verifyCredentials(username,password):
    if not userExists(username):
        return generateReturnDictionary(301,'invalid username'), False

    correct_pw = verifyPw(username,password)
    if not correct_pw:
        return generateReturnDictionary(302,"invalid password"), True

    return None, False
def generateReturnDictionary(status,message):
    return {
        "status":status,
        "message":message
    }

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

        hashed_pw = bcrypt.hashpw(password.encode('utf8'),bcrypt.gensalt())
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

class Classif(Resource):
    def post(self):
        postedData = request.get_json()
        username = postedData['username']
        password = postedData['password']
        url = postedData['url']

        retJson, error = verifyCredentials(username,password)

        if error:
            return jsonify(retJson)

        # check to see if they have enough tokens to use the API  
        tokens = users.find({'username':username})[0]['tokens']
        if tokens <= 0:
            # TODO 
            return jsonify(generateReturnDictionary(3030,'not enough tokens!'))
    
        r = requests.get(url)
        retJson = {}
        with open("temp.jpg","wb") as f:
            f.write(r.content)
            proc = subprocess.Popen("python classify_image.py --model_dir=. --image_file=./temp.jpg")
            proc.communicate()[0]
            proc.wait()
            with open("text.txt") as g:
                retJson = json.load(g)

        users.update({
            "username":username
        },{
            "$set":{
                "tokens":tokens - 1
            }
        })
        return retJson



@app.route('/')
def hello():
    return "hello"

api.add_resource(Register,'/register')
api.add_resource(Classify,'/classify')
api.add_resource(Refill,'/refill')



if __name__ == "__main__":
    app.run('0.0.0.0')
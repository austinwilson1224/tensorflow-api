# todo
from flask import Flask,request,jsonify
from flask_restful import Api,Resource

from pymongo import MongoClient


# api and app
app = Flask(__name__)
api = Api(app)

# database 
client = MongoClient('mongo://db:27017')
users = client.Users 



# registration post 
class Register(Resource):
    def post(self):
        postedData = request.get_json()
        username = postedData['username']
        password = postedData['password']

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




@app.route('/')
def hello():
    return "hello"

api.add_resource(Register,'/register')
api.add_resource(Classify,'/classify')
api.add_resource(Refill,'/refill')



if __name__ == "__main__":
    app.run('0.0.0.0')
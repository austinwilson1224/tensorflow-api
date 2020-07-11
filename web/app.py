# todo
from flask import Flask,request,jsonify
from flask_restful import Api,Resource

app = Flask(__name__)
api = Api(app)

@app.route('/')
def hello():
    return "hello"



if __name__ == "__main__":
    app.run('0.0.0.0')
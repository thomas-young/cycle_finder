from flask import Flask
from flask_restful import Resource, Api
import os
import json
from arbitrage import arbitrage
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)

class ArbitrageCycle(Resource):

    def get(self):
        path, rates = arbitrage('Liquid/ETH')

        return json.dumps(path)

api.add_resource(ArbitrageCycle, '/cycle')


if __name__ == '__main__':
    app.run(debug=True)

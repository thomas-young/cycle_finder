from flask import Flask
from flask_restful import Resource, Api
import os
import json
from arbitrage import arbitrage
from flask_cors import CORS
from random import choice

app = Flask(__name__)
api = Api(app)
CORS(app)

class ArbitrageCycle(Resource):

    def get(self):

    	coins = ['ADA', 'BTC', 'DASH', 'EOS', 'ETH', 'LTC', 'TRX', 'XLM', 'XMR', 'XRP']
    	markets = ['Binance', 'BitMEX', 'Bitfinex', 'Bithumb', 'Coinbase', 'Deribit', 'Huobi', 'Kraken', 'Kucoin', 'Liquid']

    	pairs = []

    	for market in markets:
        	for coin in coins:
            	pair = market + "/" + coin
            	pairs.append(pair)

        start_coin = choice(pairs)

        path, rates = arbitrage(start_coin, pairs)
        product = 1.000000000000000000
        for rate in rates:
        	product = rate * product
        	print(product)
        #print(product)
        return json.dumps(path)

api.add_resource(ArbitrageCycle, '/cycle')


if __name__ == '__main__':
    app.run(debug=True)

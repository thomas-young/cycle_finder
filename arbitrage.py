from math import log, exp
import json
import requests
from time import sleep

def buildGraph(data):
    # initialize dictionary of coin market pairs to their values
    values = {}

    # initialize graph, which is a dictionary where each key is a market/coin pair
    # and the value is itself a dictionary. The keys of each sub-dictionary are
    # all the other market/coin pairs, where the values are exchange rates
    graph = {}

    # coins = ['ADA', 'BTC', 'DASH', 'EOS', 'ETH', 'LTC', 'TRX', 'XLM', 'XMR', 'XRP']
    markets = ['Binance', 'BitMEX', 'Bitfinex', 'Bithumb', 'Coinbase', 'Deribit', 'Huobi', 'Kraken', 'Kucoin', 'Liquid']

    # # read json file
    # with open(file, 'r') as infile:
    #     data = json.load(infile)

    # for each coin on each market, add the value to the dictionary
    for market in markets:
        for coin in data[market]:
            values[market + "/" + coin[0]] = float(coin[1])

    for c in values:
        graph[c] = {}
        for d in values:
            rate = -log(values[c]/values[d])
            graph[c][d] = rate

    return graph, values


def bellman_ford(graph, source):
    n = len(graph)

    # initialize distance and predecessor dictionaries
    dist = {}
    pred = {}
    initialize(graph, dist, pred)

    # source distance is 0 from itself
    dist[source] = 0

    # iterate through all edges n - 1 times (length of longest potential path)
    # relaxing each edge
    for i in range(n - 1):
        for u in graph:
            for v in graph[u]:
                relax(graph, u, v, dist, pred)

    # iterate through edges again, checking for a negative cycle
    # return the path if one is found, otherwise return None
    for u in graph:
        for v in graph[u]:
            if dist[v] > dist[u] + graph[u][v]:
                return pathRetraceZ(graph, pred, v)

    return None, None


def initialize(graph, dist, pred):
    for v in graph:
        dist[v] = float('inf')
        pred[v] = None


def relax(graph, u, v, dist, pred):
    if dist[u] > dist[v] + graph[u][v]:
        dist[u] = dist[v] + graph[u][v]
        pred[u] = v


def pathRetraceZ(graph, pred, v):
    trace = [v]
    curr = pred[v]
    while pred[curr] not in trace:
        trace.append(pred[curr])
        curr = pred[curr]

    start = pred[curr]
    path = [start]
    rates = []
    curr = start

    while pred[curr] not in path:
        path.append(pred[curr])
        curr = pred[curr]

    # re-add beginning/final coin
    path.append(pred[curr])

    for i in range(len(path) - 1):
        rates.append(exp(-graph[path[i]][path[i+1]]))

    return path, rates


def printPath(path, rates):
    amount = 1
    string = "starting with {} {} coins".format(amount, path[0])
    # print(string)

    for i in range(1, len(path) - 1):
        amount *= rates[i - 1]
        string = "now {} {} coins".format(amount, path[i])
        # print(string)

    amount *= rates[-1]
    string = "now {} {} coins".format(amount, path[-1])
    # print(string)
    return amount


def arbitrage(start_coin):

    response_market_data = requests.get('https://changechain-api-heroku.herokuapp.com/data')
    curr_data = response_market_data.json()

    graph, values = buildGraph(curr_data)
    # graph, values = buildGraph('1554531720.json')
    path, rates = bellman_ford(graph, start_coin)

    if path == None:
        print("No positive cycle found")
        return

    # print(path)
    # print(rates)

    # print(printPath(path, rates))

    print(path)
    return path, rates

    # max = 0
    # starting_coin = None
    #
    # for c in values:
    #     path, rates = bellman_ford(graph, c)
    #     amnt = printPath(path, rates)
    #     if amnt > max:
    #         max = amnt
    #         starting_coin = c
    # print(max)
    # print(starting_coin)

def main():
    while True:
        arbitrage('Liquid/ETH')
        # sleep(1)

main()
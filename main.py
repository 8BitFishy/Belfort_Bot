from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import time
import math
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()

class Currency:
    def __init__(self, name, current_price, update_freq, pricelist,
                 short_average, long_average, price_alerts):
        self.name = name
        self.current_price = current_price
        self.update_freq = freq
        self.pricelist = []
        self.short_average = short_average
        self.long_average = long_average
        self.price_alerts = price_alerts

short_average_count = 10
long_average_count = 100000
freq = 1
currencies = ["dogecoin", "ethereum", "bitcoin"]
'''
def import_apikeys():
    filename = 'api_keys'
    with open(filename) as f:
        for line in f:
            keys = f.split(":")
            if keys[0] = 'coinmarketcap':
                coinmarketcapapi
'''

def retrieve_price(Currency):
    #print(f"Retreiving prices for {Currency}")
    data = cg.get_price(ids=Currency, vs_currencies='GBP')
    price = data[Currency]["gbp"]
    f = open(f"{Currency}.txt", "a")
    f.write(str(price))
    f.write("\n")
    f.close()
    return price


def Generate_Currency_Classes(currencies):
    currency_list = []
    for i in range(len(currencies)):
        Currency_Master = Currency(currencies[i], 0, freq, [], 0, 0, [])
        currency_list.append(Currency_Master)

    return currency_list

def short_average(Currency):
    short_average = []
    # if length of pricelist is less than short average count
    if len(Currency.pricelist) < short_average_count:
        # short average is average of all current data
        Currency.short_average = sum(Currency.pricelist) / len(Currency.pricelist)
    # if length of pricelist is not less than short average count
    else:
        # take average of data within short average count
        for i in range(short_average_count):
            short_average.append(Currency.pricelist[i])
        Currency.short_average = sum(short_average) / len(short_average)
    print(f"Current short average = {Currency.short_average}")
    # pricelist is longer than 1 entry
    if len(Currency.pricelist) > 1:
        # calculate percent deviation of current price from short average
        price_deviation = ((Currency.pricelist[0] - Currency.short_average) / Currency.short_average) * 100
        print(f"Price deviation = {price_deviation}%")
        if abs(price_deviation) > 10:
            print(f"Breakout! Price deviation {round(price_deviation, 2)}%")
            return
        else:
            print(f"Stable, price deviation {round(price_deviation, 2)}%")
            if price_deviation > 0:
                print("Rising...")
            else:
                print("Falling...")
            return
    else:
        print("insufficient data")
        return

def long_average(Currency):
    # if length of pricelist is less than long average count
    if len(Currency.pricelist) < long_average_count:
        # long average is average of all current data
        Currency.long_average = sum(Currency.pricelist) / len(Currency.pricelist)
    # if length of pricelist is not less than long average count
    else:
        # take average of data within long average count
        for i in range(long_average_count):
            long_average.append(Currency.pricelist[i])
        Currency.long_average = sum(long_average) / len(long_average)
    print(f"Current long average = {Currency.long_average}")
    return


def analysis(Currency):
    #if length of pricelist is not zero(i.e. data present)
    if len(Currency.pricelist) != 0:
        print(f"Analysing...")
        short_average(Currency)
        long_average(Currency)
        return
    else:
        print("insufficient data")
        return


if __name__ == "__main__":

    currency_list = Generate_Currency_Classes(currencies)

    while True:
        mins = time.gmtime(time.time()).tm_min
        print("\n\n---------------------------------------")
        print(mins)
        for Currency in currency_list:
            print("\n----------------")
            print(f"Currency = {Currency.name}", end = '')
            if mins % Currency.update_freq == 0:
                Currency.current_price = retrieve_price(Currency.name)
                print(f", current price = {Currency.current_price}")
                analysis(Currency)
                Currency.pricelist.insert(0, Currency.current_price)
                if len(Currency.pricelist) > long_average_count:
                    del Currency.pricelist[long_average_count]
                print(Currency.pricelist)

        time.sleep(60)

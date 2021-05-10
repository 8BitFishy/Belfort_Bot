from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import time
import math


class Currency:
    def __init__(self, name, current_price, update_freq, pricelist,
                 rolling_average, previous_rolling_average, long_average):
        self.name = name
        self.current_price = current_price
        self.update_freq = freq
        self.pricelist = []
        self.rolling_average = rolling_average
        self.previous_rolling_average = previous_rolling_average
        self.long_average = long_average


currencies = ["DOGE"]

headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': 'ed12a146-2bd0-49d8-86c2-239b0ba06de9',
}

session = Session()
session.headers.update(headers)

average_count = 10
freq = 2


def retrieve_price(currencies):

    print(f"Retreiving prices for {currencies}")
    currency_string = ''
    for i in currencies:
        currency_string = currency_string + i + ','
    currency_string = currency_string[:-1]
    print(currency_string)
    url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol={currency_string}&convert=GBP'

    try:
        response = session.get(url)
        data = json.loads(response.text)
        print(data)
        print(data["data"]["DOGE"]["quote"]["GBP"]["price"])
        return (data["data"]["DOGE"]["quote"]["GBP"]["price"])

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


def Generate_Currency_Classes(currencies):
    currency_list = []
    for i in range(len(currencies)):
        Currency_Master = Currency(currencies[i], 0, freq, [], 0, 0, 0)
        currency_list.append(Currency_Master)
        print(currency_list)
    return currency_list


def analysis(pricelist):
    for i in range(len(pricelist)):
        rolling_average = sum(pricelist) / len(pricelist)
        if pricelist[
                0] - previous_rolling_average > previous_rolling_average / 10:
            return


if __name__ == "__main__":

    currency_list = Generate_Currency_Classes(currencies)

    while True:
        mins = time.gmtime(time.time()).tm_min
        print(mins)
        for Currency in currency_list:
            if mins % Currency.update_freq == 0:
                Currency.price = retrieve_price(currencies)
                Currency.pricelist.insert(0, Currency.price)
                if len(Currency.pricelist) > average_count:
                    del Currency.pricelist[average_count]
                print(Currency.pricelist)

        time.sleep(60)

from requests import *
import yfinance as yf
url = "https://www.alphavantage.co/query?"
api_key = "0W6T3C4CI21913T8"
def initial_price(symbol):
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol" : symbol,
        "apikey" : api_key
    }
    resp = get(url,params)
    info = resp.json()
    keys = list(info.keys())
    info = info[keys[0]]
    price = info["05. price"]
    change = info["09. change"]
    change_percent = info["10. change percent"]
    return (price, change, change_percent)
def curr_p(symbol):
    params = {
    'symbol': symbol,
    'token' : 'bqjg667rh5r89luqvicg'
    }
    resp = get('https://finnhub.io/api/v1/quote?',params)
    resp = resp.json()
    return float(resp['c'])

def crypto_price(symbol):
    params = {
        "apikey": "OYMIDLPTGY6CAMP0",
        "function": "CURRENCY_EXCHANGE_RATE",
        "from_currency": symbol,
        "to_currency": "USD"
    }
    resp = get(url, params)
    resp = resp.json()

    return float(resp['Realtime Currency Exchange Rate']['5. Exchange Rate'])

    

    

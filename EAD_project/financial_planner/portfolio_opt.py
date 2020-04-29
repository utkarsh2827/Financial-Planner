import yfinance as yf
import pandas as pd
from pypfopt import EfficientFrontier
from pypfopt import risk_models
from pypfopt.risk_models import CovarianceShrinkage
from pypfopt import expected_returns
def get_result(l):
    data = yf.download(tickers = l, period ="max", interval = "1d",auto_adjust = True)
    data = data['Close']
    mu = expected_returns.mean_historical_return(data)
    S = CovarianceShrinkage(data).ledoit_wolf()
    ef = EfficientFrontier(mu, S)
    raw_weights = ef.max_sharpe()
    cleaned_weights = ef.clean_weights()
    data = []
    for x in cleaned_weights.keys():
        if cleaned_weights[x]!=0:
            data.append({'name':x, 'y':cleaned_weights[x] })
    answer = {
        'data': data,
        'performance': ef.portfolio_performance()
    }
    return answer
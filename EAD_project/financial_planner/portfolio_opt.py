import yfinance as yf
import pandas as pd
from pypfopt import EfficientFrontier
from pypfopt import risk_models
from pypfopt.risk_models import CovarianceShrinkage
from pypfopt import expected_returns
from pypfopt.black_litterman import BlackLittermanModel
from pypfopt.hierarchical_portfolio import HRPOpt

def get_returns(data, strategy, S, prior = None):
    if strategy == 'mean' or prior == None:
        return expected_returns.mean_historical_return(data)
    else:
        bl = BlackLittermanModel(S, absolute_views = prior)
        return bl.bl_returns()

def get_result(payload, model, return_strategy):
    tickers = " ".join(list(payload.keys()))
    data = yf.download(tickers, period ="max", interval = "1d",auto_adjust = True)
    data = data['Close']
    S = CovarianceShrinkage(data).ledoit_wolf()
    mu = get_returns(data, return_strategy, S, payload)
    if(model == "EF"):
        return get_result_Efficient_Frontier(mu, S)
    elif(model == "H"):
        return get_result_hierarchial_clustering(data, S)

def get_result_hierarchial_clustering(mu, S):
    model = HRPOpt(mu, S)
    model.optimize()
    cleaned_weights = model.clean_weights()
    data = []
    for x in cleaned_weights.keys():
        if cleaned_weights[x]!=0:
            data.append({'name':x, 'y':cleaned_weights[x] })
    answer = {
        'data': data,
        'performance': model.portfolio_performance()
    }
    return answer

def get_result_Efficient_Frontier(mu, S):
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
from django.shortcuts import render,redirect
from .models import Funds,Stock
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .fund_interaction import *
from .forms import *
import yfinance as yf
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from .alpha_vantage_interaction import *
import json
import pandas as pd
def home(request):
    return render(request, 'financial_planner/home.html',{})
class PortfolioListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Stock
    template_name = 'financial_planner/portfolio-details.html'
    context_object_name = 'assets'
    ordering = ['-date_posted']
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stocks = Stock.objects.filter(user = self.request.user)
        context['Stock'] = {}
        for stock in stocks:
            if stock.symbol in context['Stock']:
                context['Stock'][stock.symbol]['average_price'] = stock.initial_price * stock.quantity_owned + context['Stock'][stock.symbol]['average_price'] * context['Stock'][stock.symbol]['quantity_owned']
                context['Stock'][stock.symbol]['average_price'] /= (context['Stock'][stock.symbol]['quantity_owned'] + stock.quantity_owned)
                context['Stock'][stock.symbol]['quantity_owned'] += stock.quantity_owned
                context['Stock'][stock.symbol]['average_price'] = round(context['Stock'][stock.symbol]['average_price'], 2)
                continue
            d = {}
            d["id"] = stock.id
            d['name'] = stock.name
            d['symbol'] = stock.symbol
            d['average_price'] = stock.initial_price
            d['quantity_owned'] = stock.quantity_owned
            d['curr_price'] = stock.curr_price

            context['Stock'][stock.symbol] = d

        stocks = Funds.objects.filter(user = self.request.user)
        context['Funds'] = {}
        for stock in stocks:
            if stock.symbol in context['Funds']:
                context['Funds'][stock.symbol]['average_price'] = stock.investment * stock.quantity_owned + context['Funds'][stock.symbol]['average_price'] * context['Funds'][stock.symbol]['quantity_owned']
                context['Funds'][stock.symbol]['average_price'] /= (context['Funds'][stock.symbol]['quantity_owned'] + stock.quantity_owned)
                context['Funds'][stock.symbol]['quantity_owned'] += stock.quantity_owned
                context['Funds'][stock.symbol]['average_price'] = round(context['Funds'][stock.symbol]['average_price'], 2)
                continue
            d = {}
            d["id"] = stock.id
            d['name'] = stock.name
            d['symbol'] = stock.symbol
            d['average_price'] = stock.investment
            d['quantity_owned'] = stock.quantity_owned
            d['curr_price'] = stock.curr_price

            context['Funds'][stock.symbol] = d

        return context
def stock_search(request):
    return render(request,'financial_planner/stock_search.html',{})

def crypto_search(request):
    df = pd.read_csv('./media/digital_currency_list.csv')
    l = []
    for i in range(len(df)):
        l.append({
            "name": df.iloc[i, 1],
            "symbol": df.iloc[i, 0]
        })

    return render(request, 'financial_planner/crypto_search.html', {"crypto_list": l})

def crypto_analysis_page(request, symbol, name):
    context = {
        'symbol' : symbol,
        'name' : name,
        'curr_price': float(crypto_price(symbol))
    }

    return render(request,'financial_planner/crypto_analysis.html', context)

def stock_analysis_page(request,symbol,name):
    stock = yf.Ticker(symbol)
    curr_price = curr_p(symbol)
    df = stock.financials
    df = df.reset_index()
    df.columns = df.columns.astype(str)
    df = df.rename(columns ={'index':'Area Of Expense'})
    df =  json.loads(df.to_json(orient ='records'))
    df_recom = stock.recommendations.loc['2020']
    df_recom = df_recom.reset_index()
    df_recom = df_recom.loc[:,['Firm','To Grade', 'From Grade','Action']]
    df_recom = json.loads(df_recom.to_json(orient ='records'))
    df_mh = stock.major_holders[[1,0]]
    df_mh = json.loads(df_mh.to_json(orient ='records'))
    df_it = stock.institutional_holders
    df_it['Date Reported'] = df_it["Date Reported"].astype('str')
    df_it= json.loads(df_it.to_json(orient ='records'))
    context = {
        'symbol' : symbol,
        'name' : name,
        'curr_price': float(curr_price),
        'info':stock.info,
        'financials': df,
        'recommendations':df_recom,
        'major_holders': df_mh,
        'instit_holders': df_it
    }
    return render(request,'financial_planner/analysis.html', context)
class StockDetailView(LoginRequiredMixin,DetailView):
    model = Stock

class StockUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Stock
    fields = ['quantity_owned']
    
    def form_valid(self,form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    def test_func(self):
        stock = self.get_object()
        if self.request.user == stock.user:
            return True
        return False

class FundsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Funds
    fields = ['quantity_owned']
    def form_valid(self,form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    def test_func(self):
        stock = self.get_object()
        if self.request.user == stock.user:
            return True
        return False
class StockDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Stock
    success_url = '/portfolio'
    def test_func(self):
        stock = self.get_object()
        if self.request.user == stock.user:
            return True
        return False
class FundsDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Funds
    success_url = '/portfolio'
    def test_func(self):
        stock = self.get_object()
        if self.request.user == stock.user:
            return True
        return False

def about(request):
    return render(request, 'financial_planner/about.html',{})

@login_required
def stock_create(request,symbol,name,choice):
    pk = 0
    obj = Stock(symbol = symbol, name = name, choice= choice,initial_price = curr_p(symbol), user = request.user)
    if choice =="MAIN_PORTFOLIO":
        if request.method == "POST":
            s_form = StockCreationForm(request.POST, instance = obj)
            if s_form.is_valid():
                s_form.save()
                return redirect('financial_planner-portfolio-list')
        else:
            s_form = StockCreationForm(instance = obj)
        context = {
            'form':s_form
        }
        return render(request,'financial_planner/stock_form.html',context)
    else:
        return redirect('financial_planner-portfolio-list')

@login_required
def crypto_create(request,symbol,name,choice):
    pk = 0
    obj = Funds(symbol = symbol, name = name, choice= choice, investment = crypto_price(symbol), user = request.user)
    if choice =="MAIN_PORTFOLIO":
        if request.method == "POST":
            s_form = FundsCreationForm(request.POST, instance = obj)
            if s_form.is_valid():
                s_form.save()
                return redirect('financial_planner-portfolio-list')
        else:
            s_form = FundsCreationForm(instance = obj)
        context = {
            'form':s_form
        }
        return render(request,'financial_planner/funds_form.html',context)
    else:
        return redirect('financial_planner-portfolio-list')

def recommend(request):
    return render(request,'financial_planner/port_opt.html',{})

def get_history(request,symbol,period):
    print(period)
    df = yf.download(tickers=symbol, period =period,auto_adjust = True)
    df = df.iloc[::-1]
    # print(df.head())
    # df['Date'] = df['Date'].astype('str')
    df = df.to_html(table_id = 'historical')
    s = ''
    if period == '1mo':
        s = '1 Month data'
    elif period == '3mo':
        s = '3 Months data'
    elif period == '1y':
        s = '1 Year data'
    elif period == '5y':
        s = '5 years data'
    else:
        s = 'Max data'
    df = f'<h5 id = "headline">{s}</h5><br>'+df
    return HttpResponse(df)

def port_opt(request):
    stock_list = request.GET['stock_list'].split(" ")
    prior_list = request.GET['priors'].split(" ")
    model = request.GET['model']
    return_strategy = request.GET['return_strategy']
    payload = {}

    for i in range(len(stock_list)):
        if return_strategy == "mean" or len(prior_list) == 0:
            payload[stock_list[i]] = 0
        else:
            payload[stock_list[i]] = float(prior_list[i])

    from .portfolio_opt import get_result
    answer = get_result(payload, model, return_strategy)
    return JsonResponse(answer, safe = False)

def fund_search(request):
    s = get_mf_list()
    context = {
        'table':s
    }
    return render(request,'financial_planner/fund_search.html',context)

# Financial Planner

## Description
**Financial Planner** is all you need to manage and organise your financial portfolio.This website keeps track of all your stock holdings and mutual funds and informs about your net profit/loss.The client can search for any no. of  stocks available on the major US stock exchanges like NYSE and Financial planner will give a detailed summary and customisable graph based on the historical data.The client can view all stocks held under My Portfolio. It also has a unique feature of optimising among various stock options in order to maximise your profit and help the investor reach his/her financial goals. This feature is based on Markovitz Portfolio Selection Model and maximization of Sharpe Ratio.

## Installation Guide
Run below script in cmd or terminal after going in the respective directory:
```bash
pip install -r requirements.txt
```
Next install modified yfinance with src = Path to yfinance-master:
```
pip install -e src
```
To start the server go inside EAD_Project directory and run the following:
```bash
python manage.py runserver
```
Output for above command run:
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
April 27, 2020 - 21:50:24
Django version 3.0.5, using settings 'EAD_project.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```
Follow the link generated to access the website.

## Contributors
1. **Utkarsh Nigam-----BE18103080**
2. **Hardik Grover------BE18103116**


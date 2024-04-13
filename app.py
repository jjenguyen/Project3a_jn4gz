# project 3a imports
from flask import Flask, render_template, request, flash, redirect, url_for
import csv
import os

# imports from project 3
from datetime import datetime
from dataFetcher import getStockData
from graphGenerator import generate_graph
from main import preprocess_data

app = Flask(__name__)

# generate secret key
secret_key = os.urandom(24)
app.secret_key = secret_key

# get stock symbols from csv file
def get_stock_symbols():
    symbols = []
    with open('stocks.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            symbols.append(row['Symbol'])
    return symbols

# route for form page
@app.route('/', methods=['GET', 'POST'])
def index():
    symbols = get_stock_symbols()
    errors = []
    if request.method == 'POST':
        # get form data
        symbol = request.form.get('symbol')
        chart_type = request.form.get('chart_type')
        time_series = request.form.get('time_series')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        # symbol input error checking
        if not symbol:
            errors.append('Error: Symbol input cannot be empty.')
        if symbol not in symbols:
            errors.append('Error: Invalid symbol selected.')

        # chart type input error checking
        if not chart_type:
            errors.append('Error: Chart type input cannot be empty.')
        if chart_type not in ['bar', 'line']:
            errors.append('Error: Invalid chart type selected.')

        # time series input error checking
        if not time_series:
            errors.append('Error: Time series input cannot be empty.')
        if time_series not in ['intraday', 'daily', 'weekly', 'monthly']:
            errors.append('Error: Invalid time series selected.')

        # start date input error checking
        if not start_date:
            errors.append('Error: Start date input cannot be empty.')
        else:
            try:
                datetime.strptime(start_date, '%Y-%m-%d')
            except ValueError:
                errors.append('Error: Invalid start date format. Date must be in YYYY-MM-DD format.')

        # end date input error checking
        if not end_date:
            errors.append('Error: End date input cannot be empty.')
        else:
            try:
                datetime.strptime(end_date, '%Y-%m-%d')
            except ValueError:
                errors.append('Error: Invalid end date format. Date must be in YYYY-MM-DD format.')
            if start_date > end_date:
                errors.append('Error: End date must be after start date.')

        # if time series is intraday, handle interval selection
        if time_series == 'intraday':
            interval = request.form.get('interval')
            if not interval:
                errors.append('Error: Interval input cannot be empty.')
            else:
                intervals = ['1min', '5min', '15min', '30min', '60min']
                if interval not in intervals:
                    errors.append('Error: Invalid intraday interval selected.')

                if not errors:
                    api_function = f"TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}"
                    # to check if in correct format before passing through getStockData to complete url
                    print(f"Constructed URL for intraday request: {api_function}")

                    apikey = "V6BVQP0SPVJAVA6X"
                    raw_data = getStockData(symbol, api_function, apikey)

                    if not raw_data:
                        errors.append(f'Error: Failed to fetch data for {symbol}.')
                    else:
                        filtered_data = preprocess_data(raw_data, start_date, end_date)
                        if not filtered_data:
                            errors.append('Error: No data available for the selected date range.')
                        else:
                            graph_svg = generate_graph(filtered_data, chart_type, start_date, end_date, symbol)
                            return render_template('chart.html', graph_svg=graph_svg)
        if not errors:
            api_function = {
                'daily': 'TIME_SERIES_DAILY',
                'weekly': 'TIME_SERIES_WEEKLY',
                'monthly': 'TIME_SERIES_MONTHLY'
            }.get(time_series, 'TIME_SERIES_DAILY')
            apikey = "V6BVQP0SPVJAVA6X"
            raw_data = getStockData(symbol, api_function, apikey)

            if not raw_data:
                errors.append(f'Error: Failed to fetch data for {symbol}.')
            else:
                filtered_data = preprocess_data(raw_data, start_date, end_date)
                if not filtered_data:
                    errors.append('Error: No data available for the selected date range.')
                else:
                    graph_svg = generate_graph(filtered_data, chart_type, start_date, end_date, symbol)
                    return render_template('chart.html', graph_svg=graph_svg)
            
    return render_template('index.html', symbols=symbols, errors=errors)

# route for chart page
@app.route('/chart', methods=['GET'])
def chart():
    return redirect(url_for('index')) # redirect to form page if accessed directly

if __name__ == '__main__':
    app.run(debug=True)
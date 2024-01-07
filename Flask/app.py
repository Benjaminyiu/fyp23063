from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import os
import base64
from io import BytesIO
from datetime import datetime
import csv
import pytz


app = Flask(__name__)





@app.route('/', methods=['GET', 'POST'])
def index():
    return "<p>Hello, World!</p>"


"""
@app.route('/stock')
def stock():
    
    csv_path = 'data/COMBINED_STOCK_INTRADAY_DATA/Consumer_Discretionary/Auto_Manufacturing/F.csv'
    #csv_file = f'data/COMBINED_STOCK_INTRADAY_DATA/{category}/{subcategory}/{stock}.csv'
    csv_file = pd.read_csv(csv_path)
    
    # Define Plot Data 
    labels = csv_file['Date'].tolist()

    data = csv_file['Close'].tolist()

    # Return the components to the HTML template 
    return render_template(
        template_name_or_list='stock.html',
        data=data,
        labels=labels,
    )
"""    

# Route to render the plot template
@app.route('/stock', methods=['GET', 'POST'])
def plot():
    if request.method == 'POST':
        print(request.form['start_date'])
        print(request.form['end_date'])
        start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d')

        csv_path = 'data/COMBINED_STOCK_INTRADAY_DATA/Consumer_Discretionary/Auto_Manufacturing/F.csv'
        csv_file = pd.read_csv(csv_path)

        # Filter the data based on the selected date range
        csv_file['Date'] = pd.to_datetime(csv_file['Date'])
        filtered_data = csv_file.loc[(csv_file['Date'] >= start_date) & (csv_file['Date'] <= end_date)]

        # Define Plot Data
        labels = filtered_data['Date'].tolist()
        data = filtered_data['Close'].tolist()

        # Return the components to the HTML template
        return render_template(
            template_name_or_list='stock.html',
            data=data,
            labels=labels,
        )
        
    else:
        return render_template('stock.html')
    


@app.route('/candlestick', methods=['POST'])
def candlestick_chart():
    category = request.form['category']
    subcategory = request.form['subcategory']
    stock = request.form['stock']
    # Read data from CSV file
    data = []
    csv_path = f'data/COMBINED_STOCK_INTRADAY_DATA/{category}/{subcategory}/{stock}.csv'
    with open(csv_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return render_template('candlestick.html', data=data, stock=stock)


@app.route('/categories')
def categories():
    categories = get_categories()
    return render_template('category_subCategory_stock.html', categories=categories)

@app.route('/subcategories', methods=['POST'])
def subcategories():
    category = request.form['category']
    subcategories = get_subcategories(category)
    return render_template('category_subCategory_stock.html', category=category, subcategories=subcategories)

@app.route('/stocks', methods=['POST'])
def stocks():
    category = request.form['category']
    subcategory = request.form['subcategory']
    stocks = get_stocks(category, subcategory)
    return render_template('category_subCategory_stock.html', category=category, subcategory=subcategory, stocks=stocks)

def get_categories():
    categories = []
    for root, dirs, files in os.walk('data/COMBINED_STOCK_INTRADAY_DATA'):
        if root.count('/') == 1:  # Check if the current directory is one layer under the specified path
            for dir in dirs:
                categories.append(dir)
    return categories

def get_subcategories(category):
    subcategories = []
    for root, dirs, files in os.walk(f'data/COMBINED_STOCK_INTRADAY_DATA/{category}'):
        if root.count('/') == 2:  # Check if the current directory is one layer under the specified path
            for dir in dirs:
                subcategories.append(dir)
    return subcategories

def get_stocks(category, subcategory):
    stocks = []
    for root, dirs, files in os.walk(f'data/COMBINED_STOCK_INTRADAY_DATA/{category}/{subcategory}'):
        if root.count('/') == 3:  # Check if the current directory is one layer under the specified path
            for file in files:
                if file.endswith('.csv'):
                    stocks.append(os.path.splitext(file)[0])
                    #print(os.path.splitext(file)[0])
    return stocks





    
if __name__ == '__main__':
    app.run(debug=True)
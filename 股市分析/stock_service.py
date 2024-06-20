from flask import Flask, jsonify
import logging
import requests
from collections import OrderedDict
import time
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 允許所有來源的跨域請求

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_stock_data(symbol):
    API_KEY = 'ULL9VFAOK75JZIGY'
    BASE_URL = "https://www.alphavantage.co/query"
    parameters = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": API_KEY
    }
    try:
        logging.info(f"Fetching stock data for {symbol}")
        response = requests.get(BASE_URL, params=parameters)
        response.raise_for_status()  # 檢查請求是否成功
        data = response.json()
        if "Meta Data" not in data or "Time Series (Daily)" not in data:
            logging.error(f"Unexpected data format for {symbol}: {data}")
            return None
        logging.info(f"Received data for {symbol}: {data}")
        sorted_data = OrderedDict(sorted(data['Time Series (Daily)'].items(), key=lambda t: t[0], reverse=True))
        limited_data = {int(time.mktime(time.strptime(date, "%Y-%m-%d"))): {
            'open': float(values['1. open']),
            'close': float(values['4. close']),
            'high': float(values['2. high']),
            'low': float(values['3. low']),
            'volume': int(values['5. volume'])
        } for date, values in list(sorted_data.items())[:5]}
        return limited_data
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data for {symbol}: {e}")
        return None

@app.route('/api/stock/<symbol>')
def get_stock_data(symbol):
    data = fetch_stock_data(symbol)
    if data:
        logging.info(f"Fetched and returned stock data for {symbol}")
    else:
        logging.info(f"No data found for {symbol}, returning empty response")
        data = {}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5005)
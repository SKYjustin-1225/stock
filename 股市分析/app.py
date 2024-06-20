from flask import Flask, render_template, jsonify
import logging
from cachetools import TTLCache
import requests
from flask_cors import CORS

logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
CORS(app)

app.config['STOCK_DATA'] = TTLCache(maxsize=100, ttl=300) 
app.config['STOCK_NEWS'] = TTLCache(maxsize=100, ttl=300)

NEWS_SERVICE_URL = "http://localhost:5004/api/news/"
STOCK_SERVICE_URL = "http://localhost:5005/api/stock/"

def fetch_stock_data(symbol):
    try:
        response = requests.get(STOCK_SERVICE_URL + symbol)
        response.raise_for_status()
        data = response.json()
        logging.debug(f"Received stock data for {symbol}: {data}")
        return data
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch stock data for {symbol}: {e}")
        return None

def fetch_stock_news(symbol):
    try:
        response = requests.get(NEWS_SERVICE_URL + symbol)
        response.raise_for_status()
        news = response.json()
        logging.debug(f"Fetched news for {symbol}: {news}")
        return news
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching news for {symbol} from news service: {e}")
        return None

@app.route('/api/stock/<symbol>')
def get_stock_data(symbol):
    data = fetch_stock_data(symbol)
    if data:
        app.config['STOCK_DATA'][symbol] = data  # 更新
    else:
        logging.info(f"Using cached data for {symbol}")
        data = app.config['STOCK_DATA'].get(symbol, {})
    return jsonify(data)

@app.route('/api/news/<symbol>')
def get_stock_news(symbol):
    news = fetch_stock_news(symbol)
    if news:
        app.config['STOCK_NEWS'][symbol] = news  # 更新
    else:
        logging.info(f"Using cached news for {symbol}")
        news = app.config['STOCK_NEWS'].get(symbol, [])
    return jsonify(news)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5009)
from flask import Flask, jsonify
import logging
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 允許所有來源的跨域請求

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

SENTIMENT_SERVICE_URL = "http://localhost:5008/analyze"

def analyze_sentiment(url):
    try:
        response = requests.post(SENTIMENT_SERVICE_URL, json={'url': url})
        response.raise_for_status()  # 檢查請求是否成功
        data = response.json()
        sentiment = data.get('sentiment', 0)
        if sentiment > 0:
            return '正面'
        elif sentiment < 0:
            return '負面'
        else:
            return '中性'
    except requests.exceptions.RequestException as e:
        logging.error(f"Error analyzing sentiment for {url}: {e}")
        return '無'

def fetch_stock_news(symbol):
    API_KEY = 'beda10ec961442cd8bace3fc91fabea0'
    BASE_URL = "https://newsapi.org/v2/everything"
    parameters = {
        "q": symbol,
        "apiKey": API_KEY,
        "sortBy": "publishedAt",
        "language": "en"
    }
    try:
        logging.info(f"Fetching news for symbol: {symbol}")
        response = requests.get(BASE_URL, params=parameters)
        logging.info(f"Request URL: {response.url}")
        response.raise_for_status()  # 檢查請求是否成功
        data = response.json()
        logging.info(f"Response data: {data}")
        if "articles" not in data:
            logging.error(f"Unexpected data format for {symbol} news: {data}")
            return None
        logging.debug(f"Fetched news for {symbol}: {data}")
        return [{'title': article['title'], 'url': article['url'], 'sentiment': analyze_sentiment(article['url'])} for article in data['articles'][:5]]
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching news for {symbol}: {e}")
        return None

@app.route('/api/news/<symbol>')
def get_stock_news(symbol):
    print(f"接收到請求，股票符號：{symbol}")  #回傳請求的股票符號
    news = fetch_stock_news(symbol)
    if news:
        logging.info(f"Successfully fetched news for {symbol}")
    else:
        logging.error(f"Failed to fetch news for {symbol}")
        news = []
    return jsonify(news)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5004)
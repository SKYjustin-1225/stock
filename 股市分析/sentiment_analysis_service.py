from flask import Flask, request, jsonify
from textblob import TextBlob
import requests
from bs4 import BeautifulSoup
from bs4.element import Comment

app = Flask(__name__)

def tag_visible(element):
    #過濾HTML中看不到的元素
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def get_text_from_url(url):
    #從指定URL獲取文本內容
    try:
        response = requests.get(url)
        response.raise_for_status()  # 檢查請求是否成功
        soup = BeautifulSoup(response.text, 'html.parser')
        texts = soup.findAll(string=True)  # 獲取所有新聞內容
        visible_texts = filter(tag_visible, texts)  # 過濾不可見的內容
        return " ".join(t.strip() for t in visible_texts)
    except Exception as e:
        print(f"Error fetching webpage text: {e}")
        return None

@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    #分析URL內容並使用TextBlob分析情緒最後傳值
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'Missing URL parameter'}), 400

    text = get_text_from_url(url)
    if not text:
        return jsonify({'error': 'Could not fetch text from URL'}), 500

    analysis = TextBlob(text)
    sentiment = analysis.sentiment.polarity
    return jsonify({'sentiment': sentiment})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5008)
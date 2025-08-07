from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_headlines(url, tag, class_name):
    headlines = []
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.content, 'html.parser')
        for item in soup.find_all(tag, class_=class_name)[:5]:
            text = item.get_text(strip=True)
            if text:
                headlines.append(text)
    except Exception as e:
        headlines.append(f"Error fetching: {e}")
    return headlines

@app.route('/')
def index():
    news_sources = {
        "CNN": ("https://edition.cnn.com/", "span", "container__headline-text"),
        "Al Jazeera": ("https://www.aljazeera.com/news/", "h3", "gc__title"),
        "Fox News": ("https://www.foxnews.com/", "h2", "title"),
         }

    all_news = {}
    for name, (url, tag, cls) in news_sources.items():
        all_news[name] = get_headlines(url, tag, cls)

    return render_template("index.html", all_news=all_news)

if __name__ == '__main__':
    app.run(debug=True)

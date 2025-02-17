import json
import os
from flask import Flask, render_template_string
from datetime import datetime

app = Flask(__name__)

# Load Chrome history JSON
HISTORY_FILE = "History.json"  # Replace with your actual file path

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def convert_time_usec(history_data):
    for item in history_data.get('Browser History', []):
        time_sec = item['time_usec'] / 1_000_000
        dt = datetime.fromtimestamp(time_sec)
        item['date'] = dt.strftime('%A, %B %d, %Y')
        item['time'] = dt.strftime('%I:%M:%S%p')
    return history_data

HISTORY_DATA = convert_time_usec(load_history())

HTML_TEMPLATE = """
<!DOCTYPE html>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chrome History Viewer</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, sans-serif; font-size: 90%; width: 95%; height: 95%; background: #f4f4f4; }
        .history-container { max-width: 1000px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0px 0px 10px rgba(0,0,0,0.1); margin-bottom: 20px; }
        .history-item { padding: 10px; border-bottom: 1px solid #ddd; display: flex; align-items: center; }
        .history-item a { text-decoration: none; font-weight: bold; margin-left: 10px; display: flex; align-items: center; flex: 1; min-width: 0; }
        .history-item a:hover { text-decoration: underline; }
        .history-date { font-weight: bold; margin-top: 15px; margin-bottom: 15px; }
        .history-time { font-size: 0.8em; color: gray; margin-right: 20px; } 
        .history-favicon { width: 16px; height: 16px; margin-right: 5px; flex-shrink: 0; } 
        .history-title { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; flex: 1; min-width: 0; }
        .history-domain { font-size: 0.8em; color: gray; margin-left: 10px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; flex: 1; min-width: 0; }
    </style>
</head>
<body>
    <h2>Chrome History</h2>
    {% if items == 'empty' %}
        <div>No history items found.</div>
    {% else %}
        <!-- Group items by date -->
        {% set grouped_items = {} %}
        {% for item in items %}
            {% set date = item.date %}
            {% if date not in grouped_items %}
                {% set _ = grouped_items.update({date: []}) %}
            {% endif %}
            {% set _ = grouped_items[date].append(item) %}
        {% endfor %}

        <!-- Render each date group in a separate container -->
        {% for date, items_in_date in grouped_items.items() %}
            <div class="history-container">
                <div class="history-date">{{ date }}</div>
                {% for item in items_in_date %}
                    <div class="history-item">
                        <span class="history-time">{{ item.get('time', 'No Time') }}</span>
                        <img src="{{ item.favicon_url }}" alt="XX" class="history-favicon">
                        <a href="{{ item.get('url', '#') }}" target="_blank">
                            <span class="history-title">{{ item.get('title', 'No Title') }}</span>
                        </a>
                        <!-- Extract and display the domain name -->
                        {% set url = item.get('url', '') %}
                        {% if '://' in url %}
                            {% set domain = url.split('://')[1].split('/')[0] %}
                            <span class="history-domain">{{ domain }}</span>
                        {% endif %}
                    </div>
                {% endfor %}
            </div>
        {% endfor %}
    {% endif %}
</body>
</html>
"""

@app.route('/')
def index():
    history_items = HISTORY_DATA.get('Browser History', 'empty')
    return render_template_string(HTML_TEMPLATE, items=history_items)

if __name__ == '__main__':
    app.run(debug=True)

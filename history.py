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
        if 'time_usec' in item:
            time_sec = item['time_usec'] / 1_000_000
            dt = datetime.fromtimestamp(time_sec)
            item['date'] = dt.strftime('%A, %B %d, %Y')
            item['time'] = dt.strftime('%I:%M:%S%p')
    return history_data

HISTORY_DATA = convert_time_usec(load_history())

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chrome History Viewer</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; padding: 0; background: #f4f4f4; }
        .history-container { max-width: 800px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0px 0px 10px rgba(0,0,0,0.1); }
        .history-item { padding: 10px; border-bottom: 1px solid #ddd; }
        .history-item a { text-decoration: none; font-weight: bold; }
        .history-item a:hover { text-decoration: underline; }
        .history-date { font-weight: bold; margin-top: 15px; margin-bottom: 15px; }
    </style>
</head>
<body>
    <div class="history-container">
        <h2>Chrome History</h2>
        {% if items == 'empty' %}
            <div>No history items found.</div>
        {% else %}
            {% set ns = namespace(current_date='') %}
            {% for item in items %}
                {% if item.date != ns.current_date %}
                    {% set ns.current_date = item.date %}
                    <div class="history-date">{{ ns.current_date }}</div>
                {% endif %}
                <div class="history-item">
                    <a href="{{ item.get('url', '#') }}" target="_blank">{{ item.get('title', 'No Title') }}</a>
                    - <small>{{ item.get('time', 'Unknown Time') }}</small>
                </div>
            {% endfor %}
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    history_items = HISTORY_DATA.get('Browser History', 'empty')
    return render_template_string(HTML_TEMPLATE, items=history_items)

if __name__ == '__main__':
    app.run(debug=True)

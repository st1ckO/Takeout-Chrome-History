import json
import os
from flask import Flask, render_template_string

app = Flask(__name__)

# Load Chrome history JSON
HISTORY_FILE = "History.json"  # Replace with your actual file path

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

HISTORY_DATA = load_history()

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
        .history-item a { text-decoration: none; color: #007bff; }
        .history-item a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="history-container">
        <h2>Chrome History</h2>
        {% if items == 'empty' %}
            <div>No history items found.</div>
        {% else %}
            {% for item in items %}
            <div class="history-item">
                <a href="{{ item.get('url', '#') }}" target="_blank">{{ item.get('title', 'No Title') }}</a> 
                - <small>{{ item.get('time_usec', 'Unknown Time') }}</small>
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

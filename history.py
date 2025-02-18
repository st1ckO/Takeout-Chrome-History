import json
import os
from datetime import datetime
from jinja2 import Template

# Load Chrome history JSON
HISTORY_FILE = "History.json"  # Replace with your actual file path

def load_history():
    if not os.path.exists(HISTORY_FILE):
        print(f"Error: File '{HISTORY_FILE}' not found.")
        exit(1)
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        print(f"Loading history data from '{HISTORY_FILE}'...")
        return json.load(f)

def convert_time_usec(history_data):
    print("Converting time_usec to human-readable format...")
    for item in history_data.get('Browser History', {}):
        time_sec = item['time_usec'] / 1_000_000
        dt = datetime.fromtimestamp(time_sec)
        item['date'] = dt.strftime('%A, %B %d, %Y')
        item['time'] = dt.strftime('%I:%M:%S%p')
        item['month'] = dt.month
        item['year'] = dt.year
    return history_data

def extract_domain(history_data):
    print("Extracting domain names...")
    for item in history_data.get('Browser History', {}):
        url = item.get('url', '')
        if '://' in url:
            domain = url.split('://')[1].split('/')[0]
            item['domain'] = domain
    return history_data

def group_by_date(history_data):
    print("Grouping history items by date...")
    grouped_data = {}
    for item in history_data.get('Browser History', {}):
        date = item['date']
        if date not in grouped_data:
            grouped_data[date] = []
        grouped_data[date].append(item)
    return grouped_data if grouped_data else None

HISTORY_DATA = group_by_date(extract_domain(convert_time_usec(load_history())))

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chrome History Viewer</title>
    <style>
        :root {
            --background-color: #202124; 
            --text-color: #e8eaed; 
            --accent-color: #8ab4f8; 
            --border-color: #5f6368;
            --container-bg: #2d2e30; 
        }

        body {
            font-family: 'Segoe UI', Tahoma, sans-serif;
            font-size: 90%;
            background-color: var(--background-color);
            color: var(--text-color);
            margin: 0;
            padding: 0;
            height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        h2 {
            color: var(--text-color);
            margin: 20px 0;
        }

        .history-container {
            width: 95%; 
            max-width: 1200px; 
            background-color: var(--container-bg);
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }

        .history-item {
            padding: 10px;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            align-items: center;
            width: 100%; 
        }

        .history-item a {
            text-decoration: none;
            font-weight: bold;
            margin-left: 10px;
            white-space: nowrap; 
            overflow: hidden;
            text-overflow: ellipsis;
            flex: 1
            min-width: 0;
            color: var(--accent-color);
        }

        .history-item a:hover {
            text-decoration: underline;
        }

        .history-date {
            font-weight: bold;
            margin-top: 15px;
            margin-bottom: 15px;
            color: var(--text-color);
        }

        .history-time {
            font-size: 0.8em;
            color: #9aa0a6; 
            margin-right: 20px;
            flex-shrink: 0; 
        }

        .history-favicon {
            width: 16px;
            height: 16px;
            margin-right: 5px;
            flex-shrink: 0;
        }

        .history-title {
            white-space: nowrap; 
            overflow: hidden;
            text-overflow: ellipsis;
            flex: 1; 
            min-width: 0;
            color: var(--text-color);
        }

        .history-domain {
            font-size: 0.8em;
            color: #9aa0a6; 
            margin-left: 10px;
            white-space: nowrap; 
            overflow: hidden;
            text-overflow: ellipsis;
            flex: 1
            min-width: 0;
        }

        @media (max-width: 768px) {
            body {
                padding: 10px;
            }

            .history-container {
                width: 100%; 
                padding: 15px;
            }

            .history-item {
                flex-direction: row; 
                align-items: center;
            }

            .history-time {
                margin-right: 10px;
                margin-bottom: 0;
            }

            .history-domain {
                margin-left: 10px;
                margin-top: 0;
            }
        }
    </style>
</head>
<body>
    <h2>Chrome History</h2>
    {% if items == None %}
        <div>No history items found.</div>
    {% else %}
        {% for date, items_in_date in items.items() %}
            <div class="history-container">
                <div class="history-date">{{ date }}</div>
                {% for item in items_in_date %}
                    <div class="history-item">
                        <span class="history-time">{{ item.get('time', 'No Time') }}</span>
                        <img src="{{ item.favicon_url }}" alt="XX" class="history-favicon">
                        <a href="{{ item.get('url', '#') }}" target="_blank">
                            <span class="history-title">{{ item.get('title', 'No Title') }}</span>
                        </a>
                        <span class="history-domain">{{ item.get('domain', '') }}</span>
                    </div>
                {% endfor %}
            </div>
        {% endfor %}
    {% endif %}
</body>
</html>
"""

if __name__ == "__main__":
    # Render the template with the history data
    template = Template(HTML_TEMPLATE)
    history_items = HISTORY_DATA
    rendered_html = template.render(items=history_items)

    # Save the rendered HTML to a file
    with open("output.html", "w", encoding="utf-8") as file:
        file.write(rendered_html)

    print("HTML file generated successfully as 'output.html'.")

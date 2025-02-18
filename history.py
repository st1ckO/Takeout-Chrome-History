import json
import os
from datetime import datetime
from jinja2 import Template

HISTORY_FILE = input("Enter the path to your Chrome history JSON file: ")

def load_history():
    if not os.path.exists(HISTORY_FILE):
        print(f"Error: File '{HISTORY_FILE}' not found.")
        exit(1)
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        print(f"Loading history data from '{HISTORY_FILE}'...")
        history_data = json.load(f)
        if not history_data:
            print("Error: JSON is empty.")
            exit(1)
        elif 'Browser History' not in history_data:
            print("Error: JSON does not contain 'Browser History'.")
            exit(1)
        return history_data

def convert_time_usec(history_data):
    print("Converting time_usec to human-readable format...")
    for item in history_data.get('Browser History', []):
        time_sec = item['time_usec'] / 1_000_000
        dt = datetime.fromtimestamp(time_sec)
        item['date'] = dt.strftime('%A, %B %d, %Y')
        item['time'] = dt.strftime('%I:%M:%S%p')
        item['year'] = dt.year
        item['month'] = dt.month  
    return history_data

def extract_domain(history_data):
    print("Extracting domain names...")
    for item in history_data.get('Browser History', []):
        url = item.get('url', '')
        if '://' in url:
            domain = url.split('://')[1].split('/')[0]
            item['domain'] = domain
    return history_data

def group_by_date(history_data):
    print("Grouping history items by date...")
    grouped_data = {}
    for item in history_data.get('Browser History', []):
        year = item['year']
        month = item['month']
        date = item['date']  
        
        if year not in grouped_data:
            grouped_data[year] = {}
        if month not in grouped_data[year]:
            grouped_data[year][month] = {}
        if date not in grouped_data[year][month]:
            grouped_data[year][month][date] = []
        
        grouped_data[year][month][date].append(item)
    return grouped_data if grouped_data else None

HISTORY_DATA = group_by_date(extract_domain(convert_time_usec(load_history())))

MONTH_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ year }}/{{ month_name }}</title>
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
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-bottom: 20px;
            overflow-x: hidden;
        }

        h2 {
            color: var(--text-color);
            margin: 20px 0;
        }

        .history-container {
            width: 95%; 
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
            min-width: 0;
        }
        
        .header-container {
            display: flex;
            justify-content: space-between; 
            align-items: center;
            width: 100%;
            margin-left: 20px;
            margin-top: 10px;
            margin-bottom: 20px;
            padding: 10px 0; 
        }

        .header-title {
            flex: 1;
            text-align: center;
            font-size: 1.5em;
            font-weight: bold;
        }
        
        .back-button {
            background-color: var(--accent-color);
            color: var(--background-color);
            padding: 8px 16px;
            border-radius: 4px;
            text-decoration: none;
            font-weight: bold;
            transition: background-color 0.3s ease;
        }

        .back-button:hover {
            background-color: var(--border-color);
        }
    </style>
</head>
<body>
    <div class="header-container">
        <a href="../index.html" class="back-button">Back to Index</a>
        <span class="header-title">Chrome History - {{ year }}/{{ month_name }}</span>
    </div>
    {% for date, items_in_day in items.items() %}
        <div class="history-container">
        <div class="history-date">{{ date }}</div>
        {% for item in items_in_day %}
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
    <a href="../index.html" class="back-button">Back to Index</a>
</body>
</html>
"""

INDEX_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chrome History Index</title>
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
            display: flex;
            flex-direction: column;
            align-items: left;
            margin-left: 20px;
            margin-bottom: 20px;
        }

        h2 {
            color: var(--text-color);
            margin: 20px 0;
        }

        .year-links {
            display: flex;
            flex-direction: column;
            gap: 20px; 
            margin-bottom: 20px;
            width: 100%;
        }

        .year-container {
            display: flex;
            flex-direction: row;
            align-items: center;
            gap: 15px; 
            flex-wrap: wrap; 
        }

        .year-container strong {
            font-size: 1.2em;
            min-width: 80px; 
            text-align: left;
            flex-shrink: 0;
        }

        .month-links {
            display: flex;
            gap: 10px; 
            flex-wrap: wrap; 
            flex: 1;
        }

        .year-links a {
            color: var(--accent-color);
            text-decoration: none;
            padding: 10px 20px; 
            border: 1px solid var(--border-color);
            border-radius: 8px; 
            font-size: 1.1em; 
            text-align: center;
            transition: background-color 0.3s ease;
        }

        .year-links a:hover {
            background-color: var(--border-color);
        }
    </style>
</head>
<body>
    <h2>Chrome History Index</h2>
    <div class="year-links">
        {% for year, months in items.items() %}
            <div class="year-container">
                <strong>{{ year }}</strong>
                <div class="month-links">
                    {% for month in months.keys() %}
                        <a href="{{ year }}/{{ month }}.html">{{ datetime(year, month, 1).strftime('%B') }}</a>
                    {% endfor %}
                </div>
            </div>
        {% endfor %}
    </div>
</body>
</html>
"""

if __name__ == "__main__":
    output_dir = input("Enter the name of the output folder: ").strip()
    
    # Validate the output folder name
    if not output_dir:
        print("Error: Output folder name cannot be empty.")
        exit(1)
    
    # Create a directory for the output files
    os.makedirs(output_dir, exist_ok=True)

    # Render the index page
    template = Template(INDEX_TEMPLATE)
    rendered_index = template.render(items=HISTORY_DATA, datetime=datetime)
    with open(os.path.join(output_dir, "index.html"), "w", encoding="utf-8") as file:
        file.write(rendered_index)

    # Render individual month pages
    month_template = Template(MONTH_TEMPLATE)
    for year, months in HISTORY_DATA.items():
        year_dir = os.path.join(output_dir, str(year))
        os.makedirs(year_dir, exist_ok=True)
        for month, days in months.items():
            month_name = datetime(year, month, 1).strftime('%B')
            rendered_month = month_template.render(
                year=year,
                month_name=month_name,
                items=days
            )
            with open(os.path.join(year_dir, f"{month}.html"), "w", encoding="utf-8") as file:
                file.write(rendered_month)

    print(f"HTML files generated successfully in the '{output_dir}' directory.")
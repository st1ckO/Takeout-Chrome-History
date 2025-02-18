# Google Takeout's Chrome History Visualizer

Visualize and explore your Chrome browser history from Google Takeout by parsing and generating an interactive HTML index. 

**Disclaimer**: Only the 'Browser History' data of the JSON file is supported.
## Screenshots

![App Screenshot](https://i.imgur.com/02o4eMN.png)

![App Screenshot](https://i.imgur.com/aWGGYxZ.png)


## Run Locally
Follow these steps to run the application on your system:

### 1. Initial Setup
Ensure you meet all requirements by following this [setup guide](https://gist.github.com/st1ckO/e40b21b2797ce026d1dc07c8c0e22e8a).

### 2. Download Chrome History from Google Takeout
If you haven't already downloaded your history data. You can follow [this guide](https://support.google.com/accounts/answer/3024190?hl=en) from Google. You'll only need the Chrome History data which gives a JSON file.

![Google Takeout Chrome History](https://i.imgur.com/wcOMMKi.png)

Save the JSON file (Usually, it's ```History.json```) in the same directory as the extracted repository.

### 3. Run the application
Open your terminal or command prompt. Ensure that you're in the same directory as the repository. Execute the following command:
```bash
python history.py
```

Enter the name of the JSON file. Example:
```bash
Enter the path to your Chrome history JSON file: History.json
```

Enter a valid name for the output folder. Example:
```bash
Enter the name of the output folder: my_history
```

### 4. Open the index.html file
![index.html in my_history folder](https://i.imgur.com/oA0v7oM.png)

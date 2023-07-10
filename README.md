# WebSpy: Webpage Change Detector

WebSpy is a simple terminal based tool that monitors specified websites and detects any changes in their content.

It is able to store website URLs as hashes and detect if any changes occured by comparing the old hash to a new hash. It uses the requests library to download the HTML content of each webpage specified in the URL list, and BeautifulSoup library to parse the HTML content. The program also removes script and style elements, comments, and extra whitespaces from the HTML, resulting in a cleaned text version of the webpage to avoid false positives with dynamic content such as advertisments. 

## Features

- Monitors any number of websites
- Detects changes in web content
- Stores tracked URLs in a local SQLite database
- Allows the user to easily manage tracked URLs through a simple command line interface

## Installation

1. Clone this repository:
    ```
    git clone https://github.com/YourGitHubUsername/webspy.git
    ```
2. Install necessary Python packages:
    ```
    pip install -r requirements.txt
    ```
   
## Usage

1. Start the program:
    ```
    python webspy.py
    ```
2. You will see a menu with several options. Follow the prompts to use the tool.

## Tool Options

1. **List current URLs being tracked:** Lists all the websites currently being monitored.
2. **Enter a new URL to monitor:** Prompts the user to enter a new URL to monitor.
3. **Remove URL from tracked list:** Prompts the user to remove a website from the tracking list.
4. **Rerun all tracked websites for changes:** Checks all currently tracked websites for any changes.
5. **Quit:** Quits the tool.

![WebSpy Screenshot](https://github.com/username/repository/blob/main/webspy_screenshot.png)

## Requirements

This tool requires Python 3 and the following Python libraries: requests, BeautifulSoup4, hashlib, sqlite3.

